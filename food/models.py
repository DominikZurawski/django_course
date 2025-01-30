from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Item(models.Model):

    def __str__(self):
        return self.item_name

    user_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500,default="https://media.licdn.com/dms/image/v2/C5122AQGeHzVmmEvW5Q/feedshare-shrink_800/feedshare-shrink_800/0/1573460295130?e=2147483647&v=beta&t=4aXjSfZb5RmDnXMAjN0Pe3I8t3A45lD-MQFp4jUKng8")

    def get_absolute_url(self):
           return reverse("food:detail", kwargs={"pk": self.pk})