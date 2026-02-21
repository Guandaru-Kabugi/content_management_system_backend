
import resend
from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from notifications.models import Notification
from .models import WhiteListedEmails


User = get_user_model()

resend.api_key = settings.API_KEY_RESEND_EMAIL


@shared_task
def send_invite_email(whitelist_obj_id):

    whitelist_obj = WhiteListedEmails.objects.get(id=whitelist_obj_id)
    invite_link = f"http://localhost:8000/api/v1/user/register/?token={whitelist_obj.token}"

    resend.Emails.send({
        "from": "Acme <onboarding@resend.dev>",
        "to": whitelist_obj.email,
        "subject": "You're invited to register",
        "html": f"""
            <h2>You have been invited 🎉</h2>
            <p>Click the button below to complete your registration.</p>

            <a href="{invite_link}" 
               style="padding:10px 20px;background:#4CAF50;color:white;text-decoration:none;">
               Complete Registration
            </a>

            <p>This link will only work once.</p>
        """
    })