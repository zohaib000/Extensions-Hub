from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Extension, SiteSettings

def home(request):
    """Landing page showing all extensions"""
    extensions = Extension.objects.filter(is_active=True)
    featured_extensions = extensions.filter(featured=True)[:6]
    recent_extensions = extensions[:8]
    
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'featured_extensions': featured_extensions,
        'recent_extensions': recent_extensions,
        'site_settings': site_settings,
    }
    return render(request, 'home.html', context)

def extension_detail(request, slug):
    """Individual extension page"""
    extension = get_object_or_404(Extension, slug=slug, is_active=True)
    
    # Get related extensions (exclude current one)
    related_extensions = Extension.objects.filter(is_active=True).exclude(id=extension.id)[:4]
    
    context = {
        'extension': extension,
        'related_extensions': related_extensions,
    }
    return render(request, 'extension_detail.html', context)

def extensions_list(request):
    """All extensions listing page"""
    extensions = Extension.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(extensions, 12)  # Show 12 extensions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'extensions': page_obj,
    }
    return render(request, 'extensions_list.html', context)

def about_us(request):
    """About us page"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'about_us.html', context)

def contact_us(request):
    """Contact us page"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'contact_us.html', context)

def privacy_policy(request):
    """General privacy policy page"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'privacy_policy.html', context)

def terms_of_service(request):
    """General terms of service page"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'terms_of_service.html', context)

def extension_privacy_policy(request, slug):
    """Extension specific privacy policy"""
    extension = get_object_or_404(Extension, slug=slug, is_active=True)
    
    context = {
        'extension': extension,
    }
    return render(request, 'extension_privacy_policy.html', context)

def extension_terms_of_service(request, slug):
    """Extension specific terms of service"""
    extension = get_object_or_404(Extension, slug=slug, is_active=True)
    
    context = {
        'extension': extension,
    }
    return render(request, 'extension_terms_of_service.html', context)

def support(request):
    """Support page"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'support.html', context)