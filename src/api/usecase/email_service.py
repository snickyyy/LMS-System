import logging
from asyncio import sleep, create_task

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import SecretStr, EmailStr

from settings import settings

logger = logging.getLogger(__name__)

class EmailService:
    _config = ConnectionConfig(
        MAIL_USERNAME=settings.get_settings().EMAIL.USERNAME,
        MAIL_PASSWORD=SecretStr(settings.get_settings().EMAIL.PASSWORD),
        MAIL_FROM=settings.get_settings().EMAIL.FROM,
        MAIL_PORT=settings.get_settings().EMAIL.PORT,
        MAIL_SERVER=settings.get_settings().EMAIL.SERVER,
        MAIL_FROM_NAME=settings.get_settings().EMAIL.FROM_NAME,
        MAIL_STARTTLS=settings.get_settings().EMAIL.STARTTLS,
        MAIL_SSL_TLS=settings.get_settings().EMAIL.SSL_TLS,
        USE_CREDENTIALS=settings.get_settings().EMAIL.USE_CREDENTIALS,
        VALIDATE_CERTS=settings.get_settings().EMAIL.VALIDATE_CERTS,
    )
    _instance = None

    def __init__(self):
        self.fm = FastMail(self._config)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmailService, cls).__new__(cls)
        return cls._instance

    async def _send_email(self, recipients: list[str], subject: str, body: str):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.plain,
        )
        for i in range(3):
            try:
                await self.fm.send_message(message)
            except Exception as e:
                logger.error("Error sending email try: %s || error: %s", i+1, e)
                await sleep(i+1)

    async def send_register_email(self, to: str, token: str):
        s = settings.get_settings().APP
        subject = "GoCode confirm account"
        body = f"""Hi, this is a registration mail, thanks for using our service. follow the url below\nhttp://{s.APP_HOST}:{s.APP_PORT}/accounts/auth/activate-account/{token}"""
        create_task(self._send_email([to], subject, body))
