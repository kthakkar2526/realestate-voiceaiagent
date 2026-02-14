import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_booking_email(to_email: str, name: str, property_title: str,
                       visit_date: str, visit_time: str, booking_id: int):
    """Send booking confirmation email via Gmail SMTP."""
    subject = f"Visit Confirmed — {property_title}"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto;">
        <div style="background: #2563eb; color: white; padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="margin: 0;">PropertyAI</h2>
        </div>
        <div style="padding: 24px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 12px 12px;">
            <h3 style="color: #111;">Visit Confirmed!</h3>
            <p>Hi {name},</p>
            <p>Your property visit has been booked successfully.</p>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr><td style="padding: 8px 0; color: #6b7280;">Property</td>
                    <td style="padding: 8px 0; font-weight: 600;">{property_title}</td></tr>
                <tr><td style="padding: 8px 0; color: #6b7280;">Date</td>
                    <td style="padding: 8px 0; font-weight: 600;">{visit_date}</td></tr>
                <tr><td style="padding: 8px 0; color: #6b7280;">Time</td>
                    <td style="padding: 8px 0; font-weight: 600;">{visit_time}</td></tr>
                <tr><td style="padding: 8px 0; color: #6b7280;">Booking ID</td>
                    <td style="padding: 8px 0; font-weight: 600;">#{booking_id}</td></tr>
            </table>
            <p style="color: #6b7280; font-size: 14px;">We'll send you a reminder before your visit. If you need to reschedule, just chat with our AI assistant.</p>
        </div>
    </div>
    """

    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        print(f"[DEV MODE] Email to {to_email}:")
        print(f"  Subject: {subject}")
        print(f"  Property: {property_title} | Date: {visit_date} | Time: {visit_time}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, to_email, msg.as_string())
        print(f"[EMAIL] Sent booking confirmation to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def send_booking_whatsapp(to_phone: str, name: str, property_title: str,
                          visit_date: str, visit_time: str, booking_id: int):
    """Send booking confirmation via Twilio WhatsApp sandbox."""
    body = (
        f"Hi {name}! Your property visit is confirmed.\n\n"
        f"Property: {property_title}\n"
        f"Date: {visit_date}\n"
        f"Time: {visit_time}\n"
        f"Booking ID: #{booking_id}\n\n"
        f"We'll remind you before your visit. Reply here if you need to reschedule!"
    )

    if not settings.TWILIO_ACCOUNT_SID:
        print(f"[DEV MODE] WhatsApp to {to_phone}:")
        print(f"  {body}")
        return True

    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # Ensure WhatsApp format
        wa_to = to_phone if to_phone.startswith("whatsapp:") else f"whatsapp:{to_phone}"
        client.messages.create(
            body=body,
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            to=wa_to,
        )
        print(f"[WHATSAPP] Sent booking confirmation to {to_phone}")
        return True
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")
        return False


def send_booking_notifications(lead, property_title: str, visit_date: str,
                               visit_time: str, booking_id: int):
    """Send all booking notifications (email + WhatsApp) based on available contact info."""
    name = lead.name or "there"

    if lead.email:
        send_booking_email(lead.email, name, property_title, visit_date, visit_time, booking_id)

    if lead.phone:
        send_booking_whatsapp(lead.phone, name, property_title, visit_date, visit_time, booking_id)

    if not lead.email and not lead.phone:
        print(f"[NOTIFY] No contact info for lead {lead.id}, skipping notifications")
