from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
import re
from bs4 import BeautifulSoup


# Create your views here.

class CreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

         # Generate a notification
        Notification.objects.create(
            user=request.user,  # the current authenticated user
            title=instance.title,
            content=self.generate_notification_content(instance.content)
        )

        return Response(
            {"message": f"{instance.title} has been created successfully"},
            status=status.HTTP_201_CREATED
        )
    def generate_notification_content(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Replace <br> and <p> with newline
        for br in soup.find_all("br"):
            br.replace_with("\n")
        for p in soup.find_all("p"):
            p.insert_before("\n")
        
        text = soup.get_text(separator="\n", strip=True)
        
        # Normalize multiple newlines
        text = re.sub(r'\n+', '\n', text)
        
        # Optional: truncate to 150 chars
        if len(text) > 150:
            text = text[:150].rstrip() + "…"
        
        return text
    
class UpdateGetDeleteAPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": f"{instance.title} has been updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": f"{instance.title} has been deleted successfully"
            },
            status=status.HTTP_200_OK
        )
