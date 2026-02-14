from django.db import models
from django.utils import timezone
from videos.models import Tag

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )

    author = models.CharField(max_length=150, default="Jonah Western")
    title = models.CharField(max_length=200)
    date_posted = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    description = models.CharField(max_length=300)
    content = models.TextField()

    is_commentary = models.BooleanField(default=False)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Draft')
    tags = models.ManyToManyField(Tag)
    visibility = models.BooleanField(default=False)
    open_graph_image_url = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'
