# content_management_system_backend
This project will contain different endpoints needed to handle the management of content in a personal blog/website

# accounts api
Handles the registration, login, getting, deleting, and updating of a user
1. There is an endpoint that allows the creation of a superadmin, without needing to go to django admin panel. This endpoint requires authentication and the user should have the role superadmin.
2. There is an endpoint to register a regular admin user that does not have the ability to access django admin panel.
3. Deleting a user is also possible but requires the user to be a superadmin as well. 
4. I Implemented a way to update key fields like password, username, full_name, and image. Email and Role cannot be changed once a user account is created
5. I have implemented a way to get a user who is authenticated, to get details that can be dispIayed on the profile page.
[I will also need to implement a whitelist that will be compared against when creating an admin user]