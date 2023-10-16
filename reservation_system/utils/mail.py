from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from ..settings import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=settings.mail_port,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

fm = FastMail(mail_config)


async def send_email(to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype="html",
    )
    await fm.send_message(message)
