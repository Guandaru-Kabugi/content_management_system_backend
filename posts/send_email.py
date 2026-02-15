
import resend
from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from notifications.models import Notification


User = get_user_model()

resend.api_key = settings.API_KEY_RESEND_EMAIL


@shared_task
def notify_all_users(notification_id):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    formatted_content = notification.content.replace("\n", "<br>")

    if notification.action == "created":
        heading = f"🆕 A new post was published by {user.username}"
    else:
        heading = f"✏️ A post was updated by {user.username}"

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

    # for email in users:
    #     resend.Emails.send({
    #         "from": "Acme <onboarding@resend.dev>",
    #         "to": "westernjonah@gmail.com",
    #         "subject": notification.title,
    #         "html": f"""
    #             <h2>The post by the title : {notification.title} has been created by user with the email {user.email} </h2>
    #             <p>{formatted_content}</p>
    #             <hr>
    #             <small>Created on {notification.created_on.strftime("%Y-%m-%d %H:%M")}</small>
    #         """
    #     })
