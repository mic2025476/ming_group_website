# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings
from django.conf.urls.static import static

from companies import views
from companies.views import home_view  # Import static helper

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  
    path('about-us/', views.about_us, name='about_us'), 
    path('gallery/', views.gallery, name='gallery'),
    path('career/', views.career, name='career'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('footer-content/<int:id>/', views.footer_content_view, name='footer-content'), 
    path('i18n/', include('django.conf.urls.i18n')), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
