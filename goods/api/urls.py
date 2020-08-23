from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

from .views import ItemDetailAPIView, ItemListAPIView, ItemShortAPIVIew, TagListAPIView
from .yasg import urlpatterns as doc_urls

schema_view = get_swagger_view(title="Goods")

urlpatterns = [
    path("api/items/", ItemListAPIView.as_view()),
    path("api/items/short/<int:pk>", ItemShortAPIVIew.as_view()),
    url(r"api/items/(?P<pk>[0-9]+)$", ItemDetailAPIView.as_view()),
    url("api/tags/", TagListAPIView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += doc_urls
