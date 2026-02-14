
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

    users = User.objects.filter(is_active=True).exclude(email="").values_list("email", flat=True)
    user = notification.user

    # Convert newlines for HTML email
    formatted_content = notification.content.replace("\n", "<br>")
    print(f"Sending email for notification {notification.id} by {user.username}")
    print(f"HTML content:\n{formatted_content}")

    resend.Emails.send({
            "from": "Acme <onboarding@resend.dev>",
            "to": "westernjonah@gmail.com",
            "subject": notification.title,
            "html": f"""
                <h4> A Post published by {user.username}</h4>
                <br>
                <br>
                <p>{formatted_content}</p>
                <hr>
                <small>Created on {notification.created_on.strftime("%Y-%m-%d %H:%M")}</small>
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
