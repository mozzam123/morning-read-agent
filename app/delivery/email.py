import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.delivery.base import DeliveryProvider
from app.schemas.article import Article


class EmailDelivery(DeliveryProvider):

    def send(
        self,
        genre: str,
        article: Article,
        reason: str,
    ) -> None:

        if not settings.email_sender:
            raise ValueError("EMAIL_SENDER is not configured.")

        if not settings.email_password:
            raise ValueError("EMAIL_PASSWORD is not configured.")

        if not settings.email_recipient:
            raise ValueError("EMAIL_RECIPIENT is not configured.")

        message = EmailMessage()

        message["From"] = settings.email_sender
        message["To"] = settings.email_recipient
        message["Subject"] = f"☀️ Today's Read — {genre}"

        message.set_content(
            f"""
☀️ Today's Read

Topic: {genre}

{article.title}

Why this was selected:
{reason}

Read:
{article.url}
""".strip()
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
        ) as smtp:

            smtp.login(
                settings.email_sender,
                settings.email_password,
            )

            smtp.send_message(message)
