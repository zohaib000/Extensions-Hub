from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.safestring import mark_safe
import re

class Extension(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(max_length=300)
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
    meta_description = models.CharField(max_length=1000000000000000000, blank=True)
    meta_keywords = models.CharField(max_length=1000000000000000000000, blank=True)
    
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