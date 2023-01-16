from django.db import models
from companies.models import CompanyProfile
from users.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    post_likes = models.IntegerField(default=0)
    post_comments = models.IntegerField(default=0)
    def __str__(self):
        return self.body
    class Meta:
        verbose_name_plural = 'Posts'

class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.post.body
    class Meta:
        verbose_name_plural = 'Post Likes'

class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    def __str__(self):
        return self.post.body
    class Meta:
        verbose_name_plural = 'Post Comments'

@receiver(post_save, sender=PostLikes)
def increment_post_likes(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.get(pk=instance.post.pk)
        post.post_likes +=1
        post.save()
@receiver(post_save, sender=PostComments)
def increment_post_likes(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.get(pk=instance.post.pk)
        post.post_comments +=1
        post.save()
@receiver(post_delete, sender=PostLikes)
def decrement_post_likes(sender, instance, **kwargs):
    post = Post.objects.get(pk=instance.post.pk)
    post.post_likes -=1
    post.save()

