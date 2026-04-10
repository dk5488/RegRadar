"""
RegRadar — Alert Delivery Service
Section 6, Component 7: Multi-channel delivery via WhatsApp (BSP), Email (SendGrid), SMS.
"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.models import Alert, DeliveryLog
from app.models.enums import AlertStatus, DeliveryChannel

logger = get_logger(__name__)
settings = get_settings()


async def deliver_via_email(log: DeliveryLog, alert: Alert) -> bool:
    """
    Send alert via SendGrid email.
    """
    if not settings.SENDGRID_API_KEY:
        logger.warning("SendGrid API key not configured, skipping email delivery")
        return False

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=log.recipient,
            subject=alert.alert_title,
            plain_text_content=alert.alert_body,
            html_content=_format_email_html(alert),
        )

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        log.sent_at = datetime.now(timezone.utc)
        log.external_message_id = response.headers.get("X-Message-Id", "")

        if response.status_code in (200, 201, 202):
            logger.info("Email sent", recipient=log.recipient, status=response.status_code)
            return True
        else:
            log.failed_at = datetime.now(timezone.utc)
            log.error_message = f"SendGrid returned status {response.status_code}"
            return False

    except Exception as e:
        log.failed_at = datetime.now(timezone.utc)
        log.error_message = str(e)
        log.retry_count += 1
        logger.error("Email delivery failed", recipient=log.recipient, error=str(e))
        return False


async def deliver_via_whatsapp(log: DeliveryLog, alert: Alert) -> bool:
    """
    Send alert via WhatsApp Business API (BSP — e.g. Interakt).
    Section 11: Only send to users who have explicitly opted in.
    """
    if not settings.WHATSAPP_BSP_API_KEY:
        logger.warning("WhatsApp BSP API key not configured, skipping")
        return False

    try:
        import httpx

        # Interakt-style API payload (adjust for your BSP)
        payload = {
            "countryCode": "+91",
            "phoneNumber": log.recipient.lstrip("+91").lstrip("+"),
            "type": "Text",
            "data": {
                "message": alert.alert_body,
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.WHATSAPP_BSP_URL,
                json=payload,
                headers={
                    "Authorization": f"Basic {settings.WHATSAPP_BSP_API_KEY}",
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

        log.sent_at = datetime.now(timezone.utc)

        if response.status_code in (200, 201, 202):
            response_data = response.json()
            log.external_message_id = response_data.get("id", "")
            logger.info("WhatsApp message sent", recipient=log.recipient)
            return True
        else:
            log.failed_at = datetime.now(timezone.utc)
            log.error_message = f"BSP returned {response.status_code}: {response.text[:200]}"
            return False

    except Exception as e:
        log.failed_at = datetime.now(timezone.utc)
        log.error_message = str(e)
        log.retry_count += 1
        logger.error("WhatsApp delivery failed", recipient=log.recipient, error=str(e))
        return False


async def deliver_alert(log: DeliveryLog, alert: Alert, db: AsyncSession) -> bool:
    """
    Dispatch a single delivery log to the appropriate channel.
    Updates the log's status timestamps and the parent alert status.
    """
    success = False

    if log.channel == DeliveryChannel.EMAIL:
        success = await deliver_via_email(log, alert)
    elif log.channel == DeliveryChannel.WHATSAPP:
        success = await deliver_via_whatsapp(log, alert)
    elif log.channel == DeliveryChannel.SMS:
        # SMS delivery not implemented in MVP — fall back to skip
        logger.info("SMS delivery not yet implemented, skipping", recipient=log.recipient)
        return False

    # Update alert status based on delivery outcome
    if success and alert.status == AlertStatus.PENDING:
        alert.status = AlertStatus.SENT

    await db.flush()
    return success


def _format_email_html(alert: Alert) -> str:
    """Format the alert as a simple, clean HTML email."""
    body_html = alert.alert_body.replace("\n", "<br>")

    return f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
        <div style="background: linear-gradient(135deg, #0f3460 0%, #533483 100%); padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="color: white; margin: 0; font-size: 18px;">{alert.alert_title}</h2>
        </div>
        <div style="background: #f9f9f9; padding: 20px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 12px 12px;">
            <p style="line-height: 1.6;">{body_html}</p>
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="font-size: 12px; color: #888;">
                ⚠️ This alert is for informational purposes only.
                Please consult your CA or legal advisor before taking compliance action.
            </p>
            <p style="font-size: 12px; color: #888;">
                Powered by RegRadar — MSME Regulatory Intelligence Platform
            </p>
        </div>
    </body>
    </html>
    """
