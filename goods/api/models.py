from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    city = models.CharField(max_length=100)
    price = models.BigIntegerField()
    photo = models.ImageField(upload_to="items_photos/%Y/%m/%d", null=True)
    tag = models.ForeignKey(
        Tag, related_name="tag", on_delete=models.CASCADE, default=1
    )
    views = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title