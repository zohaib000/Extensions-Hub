from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F
from .models import Extension, SiteSettings, BlogPost

def home(request):
    """Landing page showing all extensions and featured blogs"""
    extensions = Extension.objects.filter(is_active=True)
    featured_extensions = extensions.filter(featured=True)[:6]
    recent_extensions = extensions[:8]
    
    # Featured blogs for homepage
    featured_blogs = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'featured_extensions': featured_extensions,
        'recent_extensions': recent_extensions,
        'featured_blogs': featured_blogs,
        'site_settings': site_settings,
    }
    return render(request, 'home.html', context)

def extension_detail(request, slug):
    """Individual extension page"""
    extension = get_object_or_404(Extension, slug=slug, is_active=True)
    
    # Get related extensions (exclude current one)
    related_extensions = Extension.objects.filter(is_active=True).exclude(id=extension.id)[:4]
    
    # Get related blog posts for this extension
    related_blogs = BlogPost.objects.filter(
        related_extension=extension, 
        is_published=True
    )[:3]
    
    context = {
        'extension': extension,
        'related_extensions': related_extensions,
        'related_blogs': related_blogs,
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

def blog_list(request):
    """Blog listing page with pagination"""
    blogs = BlogPost.objects.filter(is_published=True).select_related('related_extension', 'author')
    
    # Filter by extension if specified
    extension_filter = request.GET.get('extension')
    if extension_filter:
        blogs = blogs.filter(related_extension__slug=extension_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            title__icontains=search_query
        ).distinct()
    
    # Pagination - 30 blogs per page as requested
    paginator = Paginator(blogs, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all extensions for filter dropdown
    extensions = Extension.objects.filter(is_active=True).order_by('title')
    
    context = {
        'page_obj': page_obj,
        'blogs': page_obj,
        'extensions': extensions,
        'current_extension': extension_filter,
        'search_query': search_query,
    }
    return render(request, 'blog_list.html', context)

def blog_detail(request, slug):
    """Individual blog post page with SEO optimization"""
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    BlogPost.objects.filter(id=blog.id).update(view_count=F('view_count') + 1)
    blog.refresh_from_db()
    
    # Get related blog posts
    related_blogs = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=blog.id)
    
    # Prioritize blogs from same extension
    if blog.related_extension:
        related_blogs = related_blogs.filter(related_extension=blog.related_extension)
    
    related_blogs = related_blogs[:4]
    
    # Get recent blog posts if not enough related ones
    if len(related_blogs) < 4:
        recent_blogs = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=blog.id).exclude(
            id__in=[rb.id for rb in related_blogs]
        )[:4-len(related_blogs)]
        related_blogs = list(related_blogs) + list(recent_blogs)
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
    }
    return render(request, 'blog_detail.html', context)

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
