from rest_framework import serializers
from .models import Tag, Videos

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_on', 'updated_on']
        read_only_fields = ['id', 'created_on', 'updated_on']

class VideosSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags'
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Videos
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'cloudnary_url',
            'weblink_url',
            'thumbnail_url',
            'source',
            'posted_on',
            'updated_on',
            'status',
            'status_display',
            'tags',
            'tag_ids',
            'visibility',
            'open_graph_image_url'
        ]
        read_only_fields = ['id','posted_on', 'updated_on']
    
    def validate(self, attrs):
        if not attrs.get('cloudnary_url') and not attrs.get('weblink_url'):
            raise serializers.ValidationError("Either cloudnary_url or weblink_url must be provided.")
        return attrs
class VideosUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags'
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Videos
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'cloudnary_url',
            'weblink_url',
            'thumbnail_url',
            'source',
            'posted_on',
            'updated_on',
            'status',
            'status_display',
            'tags',
            'tag_ids',
            'visibility',
            'open_graph_image_url'
        ]
        read_only_fields = ['id','posted_on', 'updated_on']
