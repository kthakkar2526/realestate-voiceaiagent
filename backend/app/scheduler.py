"""
Follow-up scheduler using APScheduler.

Runs periodic tasks:
1. Booking reminders — notify users 1 day before their visit
2. Inactive lead follow-ups — nudge leads who haven't interacted in 24h
"""

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import Booking, Lead, Property
from app.notifications import send_booking_email, send_booking_whatsapp

scheduler = BackgroundScheduler()


def send_booking_reminders():
    """Send reminders for visits happening tomorrow."""
    db = SessionLocal()
    try:
        tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        bookings = (
            db.query(Booking)
            .filter(Booking.visit_date == tomorrow)
            .filter(Booking.status == "pending")
            .filter(Booking.reminder_sent == False)  # noqa: E712
            .all()
        )

        for booking in bookings:
            lead = db.query(Lead).filter(Lead.id == booking.lead_id).first()
            prop = db.query(Property).filter(Property.id == booking.property_id).first()
            if not lead or not prop:
                continue

            name = lead.name or "there"
            if lead.email:
                send_booking_email(
                    lead.email, name, prop.title,
                    booking.visit_date, booking.visit_time, booking.id
                )
            if lead.phone:
                send_booking_whatsapp(
                    lead.phone, name, prop.title,
                    booking.visit_date, booking.visit_time, booking.id
                )

            booking.reminder_sent = True
            print(f"[SCHEDULER] Sent reminder for booking #{booking.id} to {lead.name}")

        db.commit()
        if bookings:
            print(f"[SCHEDULER] Sent {len(bookings)} booking reminders")
    except Exception as e:
        print(f"[SCHEDULER ERROR] Booking reminders: {e}")
    finally:
        db.close()


def follow_up_inactive_leads():
    """Log inactive leads (no activity in 24h) for manual follow-up."""
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(hours=24)
        inactive_leads = (
            db.query(Lead)
            .filter(Lead.last_activity_at < cutoff)
            .filter(Lead.name.isnot(None))
            .filter(Lead.phone.isnot(None))
            .all()
        )

        for lead in inactive_leads:
            print(f"[FOLLOW-UP] Inactive lead: {lead.name} ({lead.phone}) — last active: {lead.last_activity_at}")

        if inactive_leads:
            print(f"[SCHEDULER] Found {len(inactive_leads)} inactive leads needing follow-up")
    except Exception as e:
        print(f"[SCHEDULER ERROR] Inactive leads: {e}")
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler."""
    # Run booking reminders every hour
    scheduler.add_job(send_booking_reminders, "interval", hours=1, id="booking_reminders")
    # Check inactive leads every 6 hours
    scheduler.add_job(follow_up_inactive_leads, "interval", hours=6, id="inactive_leads")
    scheduler.start()
    print("[SCHEDULER] Started — booking reminders (1h), inactive leads (6h)")


def stop_scheduler():
    """Stop the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        print("[SCHEDULER] Stopped")
