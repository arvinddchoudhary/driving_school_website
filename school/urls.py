from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.urls import path # type: ignore
from . import views
from django.contrib.auth import views as auth_views # type: ignore


urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('instructors/', views.instructors, name='instructors'),
    path('contact/', views.contact, name='contact'),
    # path('register/', views.register, name='register'),
    path('portal/', views.portal, name='portal'),
    path('logout/', views.logout, name='logout'),
    path('faq/', views.faq, name='faq'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)