from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator

# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.caption}"
        


class Author(models.Model): 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    # foreignkey is used for many to one relations

    def full_name(self):
        return f"{self.first_name} {self.last_name}" 

    def __str__(self):
        return self.full_name()


class Post(models.Model): 
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts" , null= True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,null=True, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="tags")
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True,db_index=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments")
