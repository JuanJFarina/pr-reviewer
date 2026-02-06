from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-pro"

    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_KEY: str | None = None
    AZURE_OPENAI_MODEL: str = "gpt-4-32k"
