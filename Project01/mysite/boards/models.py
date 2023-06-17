from django.db import models

# Create your models here.
from django.db import models

CATEGORY = (('FAQ', 'FAQ'), ('Inquiry', 'Inquiry'))

# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    detail = models.TextField(default='', null=True)
    writer = models.CharField(max_length=64)
    category =  models.CharField(choices=CATEGORY, max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    
class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.CharField(max_length=64)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)