from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "postgresql://postgres:root@localhost/realestate_agent"
    ADMIN_TOKEN: str = "admin-secret-change-me"
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    LANGFUSE_BASE_URL: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    TWILIO_WHATSAPP_NUMBER: str = "whatsapp:+14155238886"
    JWT_SECRET: str = "change-me-in-production"
    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    APIFY_TOKEN: str = ""
    VAPI_API_KEY: str = ""
    VAPI_PUBLIC_KEY: str = ""
    PUBLIC_URL: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
