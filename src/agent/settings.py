"""Settings for the agent."""

import os
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment and config files."""

    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_org_id: Optional[str] = Field(None, env="OPENAI_ORG_ID")
    serpapi_api_key: Optional[str] = Field(None, env="SERPAPI_API_KEY")
    azure_openai_api_key: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment: Optional[str] = Field(None, env="AZURE_OPENAI_DEPLOYMENT")
    cohere_api_key: Optional[str] = Field(None, env="COHERE_API_KEY")
    huggingface_api_token: Optional[str] = Field(None, env="HUGGINGFACE_API_TOKEN")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")

    # Environment
    env: str = Field("development", env="ENV")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Vector Store
    chroma_persist_dir: str = Field("./chroma_db", env="CHROMA_PERSIST_DIR")

    # Model settings
    model_name: str = "gpt-4o-mini"
    model_temperature: float = 0.0
    model_max_tokens: int = 2000

    # Agent settings
    agent_verbose: bool = True

    class Config:
        """Configuration for Pydantic settings."""

        env_file = ".env"
        case_sensitive = False

    @classmethod
    def load_from_yaml(cls, config_path: str = "config/settings.yaml"):
        """Load settings from YAML file and environment."""
        settings_dict = {}

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            # Flatten the nested config
            if "model" in config:
                settings_dict.update(
                    {
                        "model_name": config["model"].get("name", "gpt-4o-mini"),
                        "model_temperature": config["model"].get("temperature", 0.0),
                        "model_max_tokens": config["model"].get("max_tokens", 2000),
                    }
                )

            if "agent" in config:
                settings_dict.update(
                    {
                        "agent_verbose": config["agent"].get("verbose", True),
                    }
                )

        return cls(**settings_dict)


# Global settings instance
settings = Settings.load_from_yaml()
