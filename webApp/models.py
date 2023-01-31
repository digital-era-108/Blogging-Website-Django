from django.db import models
from froala_editor.fields import FroalaField
from .helpers import *
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible
from django.contrib.auth.models import User



class Categories(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Categories, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Category'
        ordering = ('created_at',)
    



class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Tag, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.title
    
    
    class Meta:
        verbose_name_plural = 'Tag'
        ordering = ('created_at',)
        


@python_2_unicode_compatible
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='blog')
    content = FroalaField()
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blog, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Blog'
        # ordering = ('-created_at',)




class MainBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.blog)
    
    class Meta:
        verbose_name_plural = 'MainBlog'


class NewsLetter(models.Model):
    email = models.EmailField(null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.email)
    
    class Meta:
        verbose_name_plural = 'NewLetter'


class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
        # def __str__(self) -> str:
        #     return str(self.parent)
    
    class Meta:
        verbose_name_plural = 'Comment'
        
        
        
class ReplyComment(models.Model):
    reply = models.TextField()
    parent = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return str(self.parent)
    
    class Meta:
        verbose_name_plural = 'Reply'