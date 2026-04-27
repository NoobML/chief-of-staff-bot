from twilio.rest import Client
import config

def send_message(to: str, message: str):
    """Send a WhatsApp message via Twilio."""
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=config.TWILIO_WHATSAPP_NUMBER,
        to=to,
        body=message
    )
    print(f"[WhatsApp] Sent to {to}: {message[:60]}...")


def alert_ceo(message: str):
    """Send an urgent alert to CEO's private number."""
    send_message(config.CEO_WHATSAPP, f"🚨 *Chief of Staff Alert*\n\n{message}")


def send_to_group(group_number: str, message: str):
    """Send a message back to a WhatsApp group."""
    send_message(group_number, message)