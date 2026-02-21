# content_management_system_backend
This project will contain different endpoints needed to handle the management of content in a personal blog/website

# accounts api
Handles the registration, login, getting, deleting, and updating of a user
1. There is an endpoint that allows the creation of a superadmin, without needing to go to django admin panel. This endpoint requires authentication and the user should have the role superadmin.
2. There is an endpoint to register a regular admin user that does not have the ability to access django admin panel.
3. Deleting a user is also possible but requires the user to be a superadmin as well. 
4. I Implemented a way to update key fields like password, username, full_name, and image. Email and Role cannot be changed once a user account is created. Use PATCH to make the change
5. I have implemented a way to get a user who is authenticated, to get details that can be dispIayed on the profile page.
6. The create whitelisted emails endpoints can also be used to get and list them. It requires authentication and user be a superadmin.
7. I have also implemented the functionality where is_active is turned to false if a whitelisted email is removed. The superadmin can later delete that account.
8. When a user is created, their email must first be whitelisted before being allowed to create an account.
9. I have implemented send_invite which invites added users to register 

$$ this concludes the expected architecture for accounts service per the front-end expectations. $$

# videos api (podcasts and short videos)

1. I have created endpoints that support updating, deleting, getting a single tag, and also getting a list of tags.
2. I have also implemented endpoints that support creating a new video, deleting a video, getting a single video, and getting a list of videos.
3. Importantly, since most updates will be partial, FRONT-END will need to use PATCH instead of PUT because they user will not be passing all the data at once.
4. The source field can then be used for podcasts

# article api (recent articles, archives, and publications)
1. I have implemented an endpoint that allows the creation and listing of articles, including necessary fields like tags among others. The endpoint requires jwtauthentication so the user must be in the database.
2. I have created a second endpoint that handles everything, including delete, update, or getting a single article
3. These endpoints will allow Annuar to handle the data that will be sent from the front-end
4. I will implement filtering that will enable Annuar to use the same endpoint to fetch articles, either in recent or those archived.
5. Importantly, this API will also be used on PUBLICATIONS by passing is_publication as True and then using it to filter in the front-end to display recent publications.

# posts api (commentaries and news)
1. I first implement create and display list of commentaries or news. The remaining functionality is a filter that will allow the separation between commentaries and news.
2. I have implemented triggering Notification Model which creates a new notification with details that will be used to send an email to the users.
3. I also implemented retrieving updating, and deleting of posts or commentaries.
4. The remaining part is adding to update and then testing everything
# notification api
1. I have created the endpoints that support crud operations around patch updates, deleting, creating, and getting.
2. The next step will be to implement resend_email to send emails to users when different objects are created.
3. I have also implemented updating of post capability and sending a notification

commands on celery
1. celery -A backend_cms_api worker --pool=solo --loglevel=info
2. docker run -d -p 6379:6379 redis

# Filtering Capabilities
examples of filtering queries that will be used
For Articles
1. /api/articles/?is_publication=true
2. /api/articles/?is_publication=true&recent_or_old=Recent
3. /api/articles/?is_publication=true&recent_or_old=Archive
4. /api/articles/?status=Published&visibility=true
For Posts
1. /api/v1/posts/?is_commentary=true&status=Published
2. /api/v1/posts/?is_commentary=true
3. /api/v1/posts/?status=Published
4. /api/v1/posts/?visibility=true
For Videos
1. /api/v1/videos/?source=Spotify&visibility=true&status=Draft
# Search Capabilities
For Articles
1. search by title, description
For Posts
1. Search by title, description, content
For Videos
1. Search by title, description
# Pagination
1. I have set pagination for the different lists to 25