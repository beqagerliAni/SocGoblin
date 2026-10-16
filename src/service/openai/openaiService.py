from openai import AsyncOpenAI
from pydantic import BaseModel

from src.config import OPENAI_KEY
from src.model import GeneratedSources
from src.service.openai.prompts.prompts import SOURCES_PROMPT


class OpenAiService():
    def __init__(self, model: str = "gpt-6-sol"):
        self.model = model

    async def structuredOutput[T: BaseModel](self, prompt: str, structure: type[T], instructions: str | None = None, webSearch: bool = False) -> T:
        async with AsyncOpenAI(api_key=OPENAI_KEY) as client:
            response = await client.responses.parse(
                model=self.model,
                instructions=instructions,
                input=prompt,
                text_format=structure,
                tools=[{"type": "web_search", "search_context_size": 'high'}] if webSearch else [],
            )
        if response.output_parsed is None:
            raise RuntimeError(f"openai did not return a {structure.__name__}")
        return response.output_parsed

    async def parsePrompt(self, prompt: str) -> GeneratedSources:
        return await self.structuredOutput(prompt, GeneratedSources, SOURCES_PROMPT, webSearch=True)
