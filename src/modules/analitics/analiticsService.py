from typing import Any

from fastapi import HTTPException
from typesafe_sdk import Choice, ChoiceAnswer

from src.modules.analitics.model.commentComplaints import CommentComplaintsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.modules.analitics.model.postTopicModel import PostTopicModel
from src.modules.analitics.model.shared.baseJevQuestionModel import BaseJevQuestionModel
from src.modules.analitics.util.commentStates import buildCommentStates
from src.modules.analitics.util.dummyData import loadDummyComments, loadDummyPosts
from src.modules.analitics.util.postStates import buildPostStates
from src.modules.analitics.prompt.instructionsPrompt import prompt as INSTRUCTIONS_PROMPT
from src.model.openAi.generateInstructions import GeneratedInstructions
from src.service.jev.jevService import JevService
from src.service.openai.openaiService import OpenAiService



class AnaliticsServiceClass():
    openAiService: OpenAiService
    jevService: JevService

    def __init__(self):
        self.openAiService = OpenAiService(model="gpt-6-luna")
        self.jevService = JevService()

    def topicResult(self, answer: ChoiceAnswer | None) -> dict[str, Any]:
        return {
            "topicType": answer.choice if answer else None,
            "confidence": answer.confidence if answer else None,
        }

    async def generateInstructions(self, request: GenerateInstructions) -> GeneratedInstructions:
        topics = "\n".join(f"- {topic}" for topic in request.topics)
        return await self.openAiService.structuredOutput(f"Topics:\n{topics}", GeneratedInstructions, INSTRUCTIONS_PROMPT)

    def buildQuestions(self, request: list[BaseJevQuestionModel]) -> dict[str, Choice]:
        names = [question.analiticName for question in request]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise HTTPException(status_code=400, detail=f"analiticName must be unique, duplicated: {sorted(duplicates)}")
        return self.jevService.buildChoiceQuestions(request)

    def analiticsResult(self, questions: dict[str, Choice], answers: dict[str, ChoiceAnswer] | None) -> dict[str, dict[str, Any]]:
        return {name: self.topicResult((answers or {}).get(name)) for name in questions}

    async def analyzePosts(self, request: list[PostTopicModel]):
        questions = self.buildQuestions(request)
        posts = loadDummyPosts()
        print(f"[analitics] {len(posts)} posts, questions: {list(questions)}")

        postStates = buildPostStates(posts)
        print(f"[analitics] sending {len(postStates)} posts to jev")

        postTopics, failedPosts = await self.jevService.chooseTopics(postStates, questions)
        print(f"[analitics] done: {len(postTopics)} posts, {len(failedPosts)} failed posts")

        return {
            "posts": [
                {"postUrl": post.postUrl, "text": post.text, "analitics": self.analiticsResult(questions, postTopics.get(post.postUrl))}
                for post in posts
            ],
            "failedPosts": failedPosts,
        }

    async def analyzeComments(self, request: list[CommentComplaintsModel]):
        questions = self.buildQuestions(request)
        comments = loadDummyComments()
        print(f"[analitics] {len(comments)} comments, questions: {list(questions)}")

        commentStates = buildCommentStates(comments)
        print(f"[analitics] sending {len(commentStates)} comments to jev")

        commentTopics, failedComments = await self.jevService.chooseTopics(commentStates, questions)
        print(f"[analitics] done: {len(commentTopics)} comments, {len(failedComments)} failed comments")

        return {
            "comments": [
                {"commentUrl": comment.commentUrl, "postUrl": comment.postUrl, "text": comment.commentText, "analitics": self.analiticsResult(questions, commentTopics.get(comment.commentUrl))}
                for comment in comments
            ],
            "failedComments": failedComments,
        }
