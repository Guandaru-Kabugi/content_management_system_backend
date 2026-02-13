from .models import Article
from videos.models import Tag
from rest_framework import serializers
from videos.serializers import TagSerializer


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags'
    )
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'year',
            'external_url',
            'thumbnail_url',
            'posted_on',
            'updated_on',
            'status',
            'recent_or_old',
            'tags',
            'tag_ids',
            'visibility',
            'open_graph_image_url'
        ]