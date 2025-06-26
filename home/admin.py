from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Extension, SiteSettings

@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'is_active', 'downloads', 'rating', 'created_at']
    list_filter = ['is_active', 'featured', 'created_at']
    search_fields = ['title', 'short_description']
    list_editable = ['featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'full_description'),
            'description': 'HTML formatting is supported for full description. You can include features, how-to guides, installation instructions, and any other content here using HTML.'
        }),
        ('Media', {
            'fields': ('main_image', 'screenshot_1', 'screenshot_2', 'screenshot_3', 'youtube_video_url'),
            'description': 'Add a YouTube video URL to embed a demo video on the extension page.'
        }),
        ('Links', {
            'fields': ('chrome_store_url',)
        }),
        ('Additional Content', {
            'fields': ('faq',),
            'description': 'HTML formatting supported. For FAQ, use Q: and A: format OR write in HTML.'
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Extension Policies', {
            'fields': ('privacy_policy', 'terms_of_service'),
            'classes': ('collapse',),
            'description': 'HTML formatting supported for both policies.'
        }),
        ('Settings', {
            'fields': ('is_active', 'featured', 'downloads', 'rating')
        })
    )
    
    # Make text fields larger for better HTML editing
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 12, 'cols': 80})},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }
        js = ('admin/js/html-editor.js',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_description'),
            'description': 'HTML formatting supported for site description.'
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'support_email', 'address', 'phone'),
            'description': 'HTML formatting supported for address field.'
        }),
        ('General Policies', {
            'fields': ('general_privacy_policy', 'general_terms_of_service', 'about_us'),
            'description': 'HTML formatting supported for all policy fields.'
        })
    )
    
    # Make text fields larger for better HTML editing
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 80})},
    }
    
    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SiteSettings
        return False