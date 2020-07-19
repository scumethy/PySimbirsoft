from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import F
from rest_framework import viewsets
import requests

from .models import Item, Tag
from .serializer import (
    ItemDetailSerializer,
    ItemListSerializer,
    ItemShortSerializer,
    TagSerializer,
)


class ItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer

    def get(self, request, pk, format=None):
        print(pk)
        item_obj = get_object_or_404(Item, pk=pk)
        item_obj.views = F("views") + 1
        item_obj.save()
        item_obj = get_object_or_404(Item, pk=pk)
        serializer = ItemDetailSerializer(item_obj)
        return Response(serializer.data)


class ItemListAPIView(ListCreateAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        price = self.request.query_params.get("price")
        fdate = self.request.query_params.get("fdate")
        ldate = self.request.query_params.get("ldate")
        tags = self.request.query_params.get("tags")

        if price:
            queryset = queryset.filter(price=price)
        if fdate and ldate:
            queryset = queryset.filter(created_on__range=[fdate, ldate])
        if tags:
            tags.split(",")
            queryset = queryset.filter(tag_id__in=tags)

        return queryset


class ItemShortAPIVIew(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemShortSerializer


class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
