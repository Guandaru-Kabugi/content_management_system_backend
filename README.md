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

$$ this concludes the expected architecture for accounts service per the front-end expectations. $$
# videos api

1. I have created endpoints that support updating, deleting, getting a single tag, and also getting a list of tags.
2. I have also implemented endpoints that support creating a new video, deleting a video, getting a single video, and getting a list of videos.
3. Importantly, since most updates will be partial, FRONT-END will need to use PATCH instead of PUT because they user will not be passing all the data at once.