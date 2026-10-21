# import asyncio

from src.modules.analitics.model.anliticsModel import AnaliticsModel
from src.modules.analitics.model.generateInstructions import GenerateInstructions
from src.modules.analitics.util.dummyData import loadDummyPosts
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

    async def generateInstructions(self, request: GenerateInstructions) -> GeneratedInstructions:
        topics = "\n".join(f"- {topic}" for topic in request.topics)
        return await self.openAiService.structuredOutput(f"Topics:\n{topics}", GeneratedInstructions, INSTRUCTIONS_PROMPT)

    async def analyzePosts(self, request: AnaliticsModel):
        posts = loadDummyPosts()
        print(f"[analitics] {len(posts)} posts, post topics: {request.postTopic.topics}")
        # print(f"[analitics] comment topics: {request.commentComplaints.topics}")

        postStates = buildPostStates(posts)
        # commentStates = {
        #     f"{post.postUrl}#comment{index}": state
        #     for post in posts
        #     for index, comment in enumerate(post.topComments)
        #     if (state := buildState(comment, ["text"])) is not None
        # }
        print(f"[analitics] sending {len(postStates)} posts to jev")

        postTopics, failedPosts = await self.jevService.chooseTopics(postStates, self.jevService.buildChoiceQuestion(request.postTopic))
        # (postTopics, failedPosts), (commentTopics, failedComments) = await asyncio.gather(
        #     self.jevService.chooseTopics(postStates, self.jevService.buildChoiceQuestion(request.postTopic)),
        #     self.jevService.chooseTopics(commentStates, self.jevService.buildChoiceQuestion(request.commentComplaints)),
        # )
        print(f"[analitics] done: {len(postTopics)} posts, {len(failedPosts)} failed posts")

        result = []
        for post in posts:
            postTopic = postTopics.get(post.postUrl)
            # comments = []
            # for index, comment in enumerate(post.topComments):
            #     commentTopic = commentTopics.get(f"{post.postUrl}#comment{index}")
            #     comments.append({
            #         "text": comment.text,
            #         "topicType": commentTopic.choice if commentTopic else None,
            #         "confidence": commentTopic.confidence if commentTopic else None,
            #     })
            result.append({
                "postUrl": post.postUrl,
                "text": post.text,
                "topicType": postTopic.choice if postTopic else None,
                "confidence": postTopic.confidence if postTopic else None,
                # "comments": comments,
            })
        return {
            "posts": result,
            "failedPosts": failedPosts,
            # "failedComments": failedComments,
        }
