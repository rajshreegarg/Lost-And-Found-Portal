from django.urls import reverse

from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.


class Lost_Product(models.Model):
    title =  models.CharField(max_length=20,null=False,blank=False)#input will be a string, and it is required field because of blank=False
    description = models.TextField(blank=False,null=False,default=" ")
    lostlocation = models.CharField(max_length=100,blank=False,null=False,default="")
    contact=models.IntegerField()
    active= models.BooleanField(default=True)
    #image=models.ImageField(upload_to='products/images/',blank=True,null=True)

    #image = models.FileField(upload_to="lostproducts/images/",null=True) # uses pillow library to diffrentiate b/w a normal file and an image
    slug = models.SlugField(blank=False,null=False,unique=True, default="")
    timestamp = models.DateTimeField(auto_now_add = True,auto_now=False)
    updated = models.DateTimeField(auto_now_add =False,auto_now=True)
    #user=models.ForeignKey(User, on_delete=models.CASCADE,)
    def __str__(self):
        return self.title

    class Meta:
        unique_together=('title','slug')
        ordering=["-updated"]

    def get_contact(self):
        return self.contact

    def get_absolute_url(self):
        return reverse ("single_product",kwargs={"id":self.id})

class ProductImage(models.Model):

    product=models.ForeignKey(Lost_Product,on_delete=models.CASCADE,)
    image=models.ImageField(upload_to='products/images/',blank=True,null=True)
    featured= models.BooleanField(default=False)
    active= models.BooleanField(default=False)
    thumbnail= models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add =False,auto_now=True)


    def __str__(self):
        return self.product.title

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length=100,default='')
    email = models.EmailField(max_length=100,default='')
    contact=models.IntegerField(default=0)
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    pincode=models.IntegerField(default=0)

def create_profile(sender,**kwargs) :
       if kwargs['created']:
           user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)
