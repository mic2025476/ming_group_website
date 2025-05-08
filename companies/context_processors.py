# context_processors.py
from .models import FooterContentModel

def footer_contents(request):
    """
    Add footer contents to all templates.
    """
    return {
        'footer_contents': FooterContentModel.objects.filter(is_active=True).order_by('created_at')
    }
