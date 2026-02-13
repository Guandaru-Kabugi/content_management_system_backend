from django.db import models
from videos.models import Tag
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Article (models.Model):
    OLD_NEW_CHOICES = (
        ('Recent', 'Recent'),
        ('Archive', 'Archive')
    )
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    year = models.PositiveIntegerField(validators=[
        MinValueValidator(1000),
        MaxValueValidator(9999)
    ])
    external_url = models.URLField(max_length=1000)
    thumbnail_url = models.URLField(max_length=1000, null=True,blank=True)

    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Draft')
    recent_or_old = models.CharField(max_length=50, choices=OLD_NEW_CHOICES, default="Recent")
    tags = models.ManyToManyField(Tag)
    visibility = models.BooleanField(default=False)
    open_graph_image_url = models.URLField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set archive status based on year
        if self.year < 2018:
            self.recent_or_old = "Archive"
        else:
            self.recent_or_old = "Recent"

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} published on {self.year}'