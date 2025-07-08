from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Extension, SiteSettings, BlogPost

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

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'related_extension', 'is_published', 'is_featured', 'view_count', 'publish_date']
    list_filter = ['is_published', 'is_featured', 'publish_date', 'related_extension']
    search_fields = ['title', 'content', 'meta_keywords']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content'),
            'description': 'You can copy/paste content from Word with images and formatting directly into the content field. HTML formatting is fully supported.'
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'featured_image_alt'),
        }),
        ('Extension Relationship', {
            'fields': ('related_extension',),
            'description': 'Link this blog post to a specific extension for better organization and SEO.'
        }),
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'SEO fields for better search engine ranking. Meta description should be compelling and under 160 characters.'
        }),
        ('Advanced SEO', {
            'fields': ('canonical_url', 'og_title', 'og_description'),
            'classes': ('collapse',),
            'description': 'Advanced SEO settings for social media and duplicate content management.'
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'author'),
        }),
        ('Analytics', {
            'fields': ('view_count',),
            'classes': ('collapse',),
        })
    )
    
    # Enhanced text fields with rich editing
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100, 'class': 'rich-text-editor'})},
        models.CharField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new blog post
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': (
                'admin/css/blog-admin.css',
                'https://cdn.ckeditor.com/4.16.2/standard-all/contents.css',
            )
        }
        js = (
            'admin/js/blog-editor.js',
            'https://cdn.ckeditor.com/4.16.2/full-all/ckeditor.js',
        )

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