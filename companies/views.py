import os
from django.shortcuts import get_object_or_404, render
from .models import FooterContentModel, HomePageContentModel, MainCompanyModel, GroupModel, StoreAddressModel

def home_view(request):
    # Fetch main company details
    main_company = MainCompanyModel.objects.filter(is_active=True, is_deleted=False).first()

    # Fetch groups with their companies and stores along with gallery images
    groups = GroupModel.objects.filter(is_active=True, is_deleted=False).prefetch_related(
        'companies__stores__gallery_images'
    )
    sections = HomePageContentModel.objects.filter(is_active=True)
    footer_contents = FooterContentModel.objects.filter(is_active=True)
    

    return render(request, 'home.html', {
        'main_company': main_company,
        'groups': groups,
        'sections': sections,
        'footer_contents': footer_contents
    })

def about_us(request):
    main_company = MainCompanyModel.objects.filter(is_active=True, is_deleted=False).first()
    return render(request, 'about_us.html', {
        'main_company': main_company
    })

def gallery(request):
    groups = GroupModel.objects.filter(is_active=True, is_deleted=False).prefetch_related(
        'companies__stores__gallery_images'
    )
    return render(request, 'gallery.html', {
        'groups': groups,
    })

def career(request):
    """
    Renders the Career page which embeds a specific Personio job post via an iframe.
    """
    job_url = "https://ming-gruppe.jobs.personio.de/job/1549141?language=en&display=de"
    return render(request, 'career.html', {'job_url': job_url})

def contact_us(request):
    return render(request, 'contact_us.html')


def footer_content_view(request, id):
    """
    View to display specific footer content based on ID.
    """
    footer_content = get_object_or_404(FooterContentModel, id=id, is_active=True)
    return render(request, 'footer_content.html', {'footer_content': footer_content})