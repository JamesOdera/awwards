from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from .views import PostListView, PostCreateView

urlpatterns=[
    url(r'^$',PostListView.as_view(),name = 'index'),
    url(r'^post/new/',PostCreateView.as_view(),name = 'post-create'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)