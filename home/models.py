from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import re

class Extension(models.Model):
    title = models.CharField(max_length=2550000)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(max_length=2550000)
    full_description = models.TextField(help_text="HTML formatting supported - You can include features, how-to-use, installation guide, and any other content here using HTML")
    
    # Images
    main_image = models.ImageField(upload_to='extensions/images/')
    screenshot_1 = models.ImageField(upload_to='extensions/screenshots/', blank=True, null=True)
    screenshot_2 = models.ImageField(upload_to='extensions/screenshots/', blank=True, null=True)
    screenshot_3 = models.ImageField(upload_to='extensions/screenshots/', blank=True, null=True)
    
    # Video
    youtube_video_url = models.URLField(
        blank=True, 
        null=True,
        help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID or https://youtu.be/VIDEO_ID)"
    )
    
    # Links
    chrome_store_url = models.URLField()
    
    # Extension specific content (HTML formatting supported)
    faq = models.TextField(blank=True, null=True, help_text="Use Q: and A: format OR HTML formatting")
    
    # SEO
    meta_description = models.CharField(max_length=2550000, blank=True)
    meta_keywords = models.CharField(max_length=2550000, blank=True)
    
    # Extension specific policies (HTML formatting supported)
    privacy_policy = models.TextField(help_text="HTML formatting supported")
    terms_of_service = models.TextField(help_text="HTML formatting supported")
    
    # Status and timestamps
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    downloads = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    class Meta:
        ordering = ['-featured', '-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('extension_detail', kwargs={'slug': self.slug})
    
    def get_youtube_embed_id(self):
        """Extract YouTube video ID from URL for embedding"""
        if not self.youtube_video_url:
            return None
        
        # Handle different YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_video_url)
            if match:
                return match.group(1)
        
        return None
    
    def get_youtube_embed_url(self):
        """Get YouTube embed URL"""
        video_id = self.get_youtube_embed_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        return None
    
    def get_faq_items(self):
        """
        Parse FAQ content into Q&A pairs
        Expected format: 
        Q: Question 1
        A: Answer 1
        
        Q: Question 2
        A: Answer 2
        """
        if not self.faq:
            return []
        
        # If contains HTML tags, return None to render as HTML
        if '<' in self.faq and '>' in self.faq:
            return None
        
        faq_items = []
        lines = self.faq.split('\n')
        current_q = None
        current_a = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                # Save previous Q&A if exists
                if current_q and current_a:
                    faq_items.append({
                        'question': current_q,
                        'answer': '\n'.join(current_a).strip()
                    })
                # Start new question
                current_q = line[2:].strip()
                current_a = []
            elif line.startswith('A:'):
                current_a.append(line[2:].strip())
            elif current_q and line:  # Continue answer
                current_a.append(line)
        
        # Add the last Q&A
        if current_q and current_a:
            faq_items.append({
                'question': current_q,
                'answer': '\n'.join(current_a).strip()
            })
        
        return faq_items


class BlogPost(models.Model):
    title = models.CharField(max_length=200000, help_text="SEO optimized blog title")
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated from title")
    
    # Content
    content = models.TextField(help_text="Full HTML formatting supported - You can copy/paste from Word with images and formatting")
    excerpt = models.TextField(max_length=200000, help_text="Short description for blog listing and social media")
    
    # SEO Fields
    meta_title = models.CharField(max_length=200000, blank=True, help_text="SEO title (60 chars max) - Leave blank to use main title")
    meta_description = models.TextField(max_length=200000, help_text="SEO meta description (160 chars max)")
    meta_keywords = models.TextField(help_text="SEO keywords separated by commas (as many as needed)")
    
    # Featured Image
    featured_image = models.ImageField(upload_to='blog/images/', help_text="Main blog image for listings and social media")
    featured_image_alt = models.CharField(max_length=200000, blank=True, help_text="Alt text for featured image (SEO)")
    
    # Relationships
    related_extension = models.ForeignKey(Extension, on_delete=models.SET_NULL, null=True, blank=True, help_text="Link this blog to a specific extension")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    # Publishing
    is_published = models.BooleanField(default=False, help_text="Publish this blog post")
    is_featured = models.BooleanField(default=False, help_text="Feature this blog on homepage")
    publish_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    # Additional SEO
    canonical_url = models.URLField(blank=True, help_text="Canonical URL if this content exists elsewhere")
    og_title = models.CharField(max_length=200000, blank=True, help_text="Open Graph title for social media")
    og_description = models.TextField(max_length=200000, blank=True, help_text="Open Graph description for social media")
    
    class Meta:
        ordering = ['-is_featured', '-publish_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-fill SEO fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.og_title:
            self.og_title = self.title[:100]
        if not self.og_description:
            self.og_description = self.excerpt[:200]
        if not self.featured_image_alt:
            self.featured_image_alt = f"Blog post about {self.title}"
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def get_seo_title(self):
        """Return meta_title if set, otherwise main title"""
        return self.meta_title if self.meta_title else self.title
    
    def get_reading_time(self):
        """Estimate reading time based on content length"""
        word_count = len(self.content.split())
        reading_time = max(1, round(word_count / 200))  # Average 200 words per minute
        return f"{reading_time} min read"
    
    def get_keywords_list(self):
        """Return keywords as a list"""
        return [keyword.strip() for keyword in self.meta_keywords.split(',') if keyword.strip()]

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Chrome Extensions Hub")
    site_description = models.TextField(help_text="HTML formatting supported")
    contact_email = models.EmailField()
    support_email = models.EmailField()
    
    # General policies (for the main site) - HTML formatting supported
    general_privacy_policy = models.TextField(help_text="HTML formatting supported")
    general_terms_of_service = models.TextField(help_text="HTML formatting supported")
    about_us = models.TextField(help_text="HTML formatting supported")
    
    # Contact info
    address = models.TextField(blank=True, help_text="HTML formatting supported")
    phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name