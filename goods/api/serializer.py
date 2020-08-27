from rest_framework.serializers import ModelSerializer

from .models import Item, Tag


class ItemDetailSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemShortSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "title",
            "city",
            "price",
        ]


class ItemListSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "user_id",
            "title",
            "description",
            "city",
            "price",
            "photo",
            "views",
            "created_on",
        ]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
