from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_shop = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class HashTag(models.Model):
    tag_name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return str(self.tag_name)



class ShopCategory(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    allowed_hash_tags = models.ManyToManyField(HashTag)
    def __str__(self):
        return str(self.category_name)

# class AllowedHashTags(models.Model):
#     shop_category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
#     hash_tags = models.ManyToManyField(HashTag)
#     def __str__(self):
#         return str(self.hash_tags)


class Shop(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ShopOwner = models.CharField(max_length=255)
    ShopName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    NumOfAds = models.IntegerField()
    NumOfQuickAds = models.IntegerField()
    ProfilePic = models.ImageField(upload_to="profilePics/")

    CreatedAt = models.DateField(auto_now_add=True)
    shop_category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
    # hash_tags = models.ManyToManyField(AllowedHashTags, blank=True)
    hash_tags = models.ManyToManyField(HashTag)
    def __str__(self):
        return str(self.ShopName)



class Advertisement(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    Advertisement_text = models.CharField(max_length=255)
    Advertisement_data = models.ImageField(upload_to="adds/")
    hash_tags = models.ManyToManyField(HashTag, blank=True)
    CreatedAt = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Advertisement_text


class QuickAdd(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    QuickAdd_text = models.CharField(max_length=255)
    QuickAdd_data = models.ImageField(upload_to="quick_adds/")
    hash_tags = models.ManyToManyField(HashTag, blank=True)
    CreatedAt = models.DateField(auto_now_add=True, db_index=True)
    def __str__(self):
        return "QuickAdd: "+self.QuickAdd_text


class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.user.username)


class Follow(models.Model):
    following = models.ForeignKey(User, related_name="user_from", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="user_to", on_delete=models.CASCADE)
    follow_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.follow_time)

