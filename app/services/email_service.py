import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(to: str, subject: str, body_html: str) -> bool:
    try:
        if not settings.SENDGRID_API_KEY:
            logger.error("SENDGRID_API_KEY no está configurada")
            return False

        if not settings.SENDGRID_FROM_EMAIL:
            logger.error("SENDGRID_FROM_EMAIL no está configurado")
            return False

        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails= to,  
            subject=subject,
            html_content=body_html
        )

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        response = sg.send(message)


        logger.info(f"SendGrid status code: {response.status_code}")
        logger.info(f"SendGrid response body: {response.body}")
        logger.info(f"SendGrid headers: {response.headers}")

        if response.status_code == 202:
            logger.info(f"Email enviado exitosamente a {to}")
            return True
        else:
            logger.warning(
                f"SendGrid respondió con status {response.status_code} para {to}"
            )
            return False

    except Exception as e:
        logger.exception(f"Error enviando email a {to}")
        return False