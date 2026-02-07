from pathlib import Path
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"

    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_KEY: str | None = None
    AZURE_OPENAI_MODEL: str = "gpt-5.2"

    @property
    def CODING_RULES_PATH(self) -> Path:
        return Path(__file__).parent.parent / "coding_rules"


Settings = _Settings()
