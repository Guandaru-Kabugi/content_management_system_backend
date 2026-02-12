from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Videos (models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creator = models.CharField(max_length=50)
    cloudnary_url = models.URLField(max_length=1000, blank=True, null=True)
    weblink_url = models.URLField(max_length=1000, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=1000, null=True,blank=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Draft')
    tags = models.ManyToManyField(Tag)
    visibility = models.BooleanField(default=False)
    open_graph_image_url = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.creator}'
