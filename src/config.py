import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

MINDCASE_KEY = os.getenv("MINDCASE_KEY")
MINDCASE_BASE_URL = os.getenv("MINDCASE_BASE_URL")
JEV_KEY = os.getenv("JEV_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
