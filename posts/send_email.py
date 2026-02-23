
from time import time

import resend
from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from notifications.models import Notification


User = get_user_model()

resend.api_key = settings.API_KEY_RESEND_EMAIL



def notify_all_users(notification_id, retries=5):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    formatted_content = notification.content.replace("\n", "<br>")

    if notification.action == "created":
        heading = f"🆕 A new post was published by {user.username}"
    else:
        heading = f"✏️ A post was updated by {user.username}"
    
    for attempt in range(retries):
        try:
            resend.Emails.send({
        "from": "Acme <onboarding@resend.dev>",
        "to": "westernjonah@gmail.com",
        "subject": notification.title,
        "html": f"""
            <h3>{heading}</h3>
            <h4>{notification.title}</h4>
            <br>
            <p>{formatted_content}</p>
            <hr>
            <small>{notification.action.capitalize()} on 
            {notification.created_on.strftime("%Y-%m-%d %H:%M")}</small>
        """
    })
            break  # Exit loop if email sent successfully
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue  # Retry
            else:
                raise e  # Raise exception if all retries fail