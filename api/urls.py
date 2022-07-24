from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import *
from . import views

urlpatterns = [
    path('characterize/', views.characterize, name = 'characterize_api'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)