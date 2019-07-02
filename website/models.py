from django.db import models
import json
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class State(BaseModel):
    name = models.TextField()
    def as_json(self):
        return json.dumps({"id":self.id,"name":self.name})
class Major(BaseModel):
    name = models.TextField()
    m_type = models.IntegerField()

    def as_json(self):
        return json.dumps({"id":self.id,"name":self.name,"type":self.m_type})
class AriaMedicUserManager(BaseUserManager):

    def create_user(self, phoneNumber, password, **extra_fields):
        """
        Creates and saves a User with the given PhoneNumber and password.
        """
        if not phoneNumber:
            raise ValueError('The phoneNumber must be set')

        user = self.model(phone_number=phoneNumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phoneNumber, password,isStaf, **extra_fields):
        if isStaf:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phoneNumber, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True,blank=True)
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11,unique=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    major = models.ForeignKey(Major,on_delete=models.CASCADE,null=True,blank=True)
    profile_image = models.ImageField(null=True,blank=True)
    level = models.IntegerField(default=0)
    qty = models.IntegerField(default=1)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'phone_number'
    objects = AriaMedicUserManager()

    def __str__(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

    def get_phone_number(self):
        return self.phone_number
class Category(BaseModel):
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    title = models.TextField()
    description = models.TextField()

    def as_json(self):
        if self.parent:
            return {"id":self.id,"title":self.title,"description":self.description,
             "parentId":self.parent.id, "parentTitle": self.parent.title,
            "parentDescription": self.parent.description}
        else:
            return {"id": self.id, "title": self.title, "description": self.description}
class Tag(BaseModel):
    name = models.TextField()
    description = models.TextField()
    def as_json(self):
        return {"id":self.id,"name":self.name,"description":self.description}
class Publisher(BaseModel):
    title = models.TextField()
    description = models.TextField()
    backgrount_image = models.ImageField(null=True,blank=True,upload_to="uploads/images/background")
    profile_image = models.ImageField(null=True,blank=True,upload_to="uploads/images/profile")
    link = models.TextField()
    def as_json(self):

        return {"id":self.id,"title":self.title,"description":self.description
                           ,"backgroundImage":self.backgrount_image.url,"profileImage":self.profile_image.url
                           ,"link":self.link}
class Discount(BaseModel):
    code = models.TextField()
    percent = models.IntegerField()
    expire_date = models.DateField()
    try_count = models.IntegerField()
    description = models.TextField()

    def as_json(self):
        return {"id": self.id, "code": self.code, "percent": self.percent
                              , "expire_date": self.expire_date, "try_count": self.try_count
                              , "description": self.description}
class Ban(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ban_time = models.DateTimeField()
    description = models.TextField()
class Ads(BaseModel):

    link = models.TextField()
    title = models.TextField()
    ads_location = models.TextField()
    ads_show_type = models.TextField()
    start_date = models.DateTimeField()
    expire_date = models.DateTimeField()
    image = models.ImageField(upload_to='uploads/images/ads')
    def as_json(self):
        return {"id":self.id,"link":self.link,"title":self.title,"ads_location":self.ads_location,"ads_show_type":self.ads_show_type,
                           "start_date":self.start_date,"expire_date":self.expire_date,"image":self.image}
class Product(BaseModel):
    product_name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE)
    discount_percent = models.IntegerField(null=True,blank=True)
    discount_time = models.DateTimeField(null=True,blank=True)
    refrence = models.TextField()
    system_code = models.TextField()
    is_active = models.BooleanField()
    sell_type = models.IntegerField()

class ProductCategory(BaseModel):
    product = models.ForeignKey(Product, related_name='category', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/images/products")

class Animation(BaseModel):
    title = models.TextField()
    file = models.FileField(upload_to="uploads/animations")
    company = models.TextField()
    publish_date = models.DateTimeField()
    time_duration = models.TextField()
    language = models.TextField()
    product = models.ForeignKey(Product,related_name="animations", on_delete=models.CASCADE)

class Article(BaseModel):
    image = models.ImageField(upload_to="uploads/images/article")
    title = models.TextField()
    description = models.TextField()
    publish_date = models.DateTimeField()
    is_active = models.BooleanField()

class Video(BaseModel):
    title = models.TextField()
    file = models.FileField(upload_to="uploads/videos")
    teacher = models.TextField()
    publish_date = models.DateTimeField()
    time_duration = models.TextField()
    language = models.TextField()
    product = models.ForeignKey(Product,related_name="videos", on_delete=models.CASCADE)
class Sound(BaseModel):
    title = models.TextField()
    file = models.FileField(upload_to="uploads/sounds")
    teacher = models.TextField()
    publish_date = models.DateTimeField()
    time_duration = models.TextField()
    language = models.TextField()
    product = models.ForeignKey(Product,related_name="sounds", on_delete=models.CASCADE)
class Quize(BaseModel):
    title = models.TextField()
    file = models.FileField(upload_to="uploads/quizes")
    teacher = models.TextField()
    publish_date = models.DateTimeField()
    question_count = models.IntegerField()
    language = models.TextField()
    product = models.ForeignKey(Product,related_name="quizes", on_delete=models.CASCADE)
class Book(BaseModel):
    title = models.TextField()
    file = models.FileField(upload_to="uploads/books")
    teacher = models.TextField()
    publish_date = models.DateTimeField()
    page_count = models.IntegerField()
    language = models.TextField()
    product = models.ForeignKey(Product,related_name="books", on_delete=models.CASCADE)
class Barrow(BaseModel):
    reciver = models.ForeignKey(User,related_name="reciver",on_delete=models.CASCADE)
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    expire_date = models.DateTimeField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Comment(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField()
    isConfirmed = models.BooleanField()

class CommentVote(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    type = models.IntegerField()
class Factor(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    factorNumber = models.IntegerField()
    status = models.IntegerField()
    trackingCode = models.IntegerField()
class FactorProducts(BaseModel):
    factor = models.ForeignKey(Factor,related_name='products',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
class Order(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    factor = models.ForeignKey(Factor,on_delete=models.CASCADE)




@receiver(post_delete, sender=Publisher)
def submission_delete(sender, instance, **kwargs):
    instance.profile_image.delete(False)
    instance.backgrount_image.delete(False)