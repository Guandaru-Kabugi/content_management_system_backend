from .models import Post
from rest_framework import serializers
from videos.serializers import TagSerializer
from videos.models import Tag
from .sanitize_html import sanitize_html_content

class PostSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags', required=False
    )

    def validate_content(self, value):
        return sanitize_html_content(value)
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'author',
            'date_posted',
            'date_updated',
            'description',
            'content',
            'status',
            'tags',
            'tag_ids',
            'visibility',
            'is_commentary',
            'open_graph_image_url'
        ]
        read_only_fields = ['id', 'date_updated']