from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nominees/', views.nominees, name='nominees'),
    path('app/<int:id>/<slug>/', views.post_detail, name='post_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
