from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MaxLengthValidator
from django.urls import reverse
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT



##########################
# end of library #
###########################

User = get_user_model()

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='1')
        
class Articles(models.Model):
    title = models.CharField(max_length=255,unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title',unique=True,unique_for_date='published')
    content = CKEditor5Field('Content', config_name='extends')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='berita/',default='logo.png',null=True)
    imagecaption = models.CharField(max_length=255,null=True,default='None')
    status = models.IntegerField(choices=STATUS, default=0)
    objects = models.Manager()
    publishedx = PublishedManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-published']
        
    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
        return reverse("article_detail",args=[self.published.year,self.published.month,self.published.day,self.slug])
    
  
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
 

class Pages(models.Model):
    title = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='title',unique=True)
    content = CKEditor5Field('Content', config_name='extends')
    status = models.IntegerField(choices=STATUS, default=0)
    
    def __str__(self):
        return self.title
     
class Comment(models.Model):
    articles = models.ForeignKey(Articles,on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.articles}' 

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
    
