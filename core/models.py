from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    catalog = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,default='zenithal')
    
    def __str__(self):
        return self.catalog
    
    class Meta:
        ordering=('-catalog',)

    def get_absolute_url(self):
       return reverse("zenithal:category",args=[self.slug])

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media_image',blank=True, null=True)
    video= models.FileField(upload_to='videos', null=True,blank=True)
    title = models.CharField(max_length=200)
    context = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering=('-created_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

   
    def get_absolute_url(self):
        return reverse("zenithal:post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title