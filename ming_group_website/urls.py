# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings
from django.conf.urls.static import static

from companies.views import maintenance_view, menu_view  # Import maintenance view and menu view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', maintenance_view, name='maintenance'),
    path('about-us/', maintenance_view, name='about_us'),
    path('gallery/', maintenance_view, name='gallery'),
    path('career/', maintenance_view, name='career'),
    path('contact_us/', maintenance_view, name='contact_us'),
    path('footer-content/<int:id>/', maintenance_view, name='footer-content'),
    path('m1/menu/', menu_view, name='m1_menu'),  # Ming menu viewer
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
