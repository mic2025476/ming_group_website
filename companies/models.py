from django.db import models

class MainCompanyModel(models.Model):
    """Represents the main company, such as Ming Group."""
    title = models.CharField(max_length=255, unique=True)  # e.g., Ming Group
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Description of the main company
    logo_path = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # Optional main company address
    contact_email = models.EmailField(blank=True, null=True)  # Main company contact email
    contact_phone = models.CharField(max_length=50, blank=True, null=True)  # Main company phone
    our_story = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GroupModel(models.Model):
    """Represents groups such as Ming Family or Han Family."""
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)  # e.g., Chinese Gastro
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyModel(models.Model):
    """Represents companies under a group."""
    group = models.ForeignKey(
        GroupModel, 
        on_delete=models.CASCADE, 
        related_name='companies', 
        blank=True, 
        null=True
    )  # Optional relationship for companies that belong to a group
    title = models.CharField(max_length=255, unique=True)  # e.g., Ming East, Ming West
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Description of the company
    logo_path = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class StoreAddressModel(models.Model):
    """Represents store-specific details for each company."""
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='stores')
    store_name = models.CharField(max_length=255,null=False,default='')
    address = models.TextField()  # Address line
    opening_hours = models.CharField(max_length=255)  # e.g., Mon - Sun: 12 PM - 10 PM
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    capacity = models.CharField(max_length=100, blank=True, null=True)  # e.g., 160 people + 100 terrace
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.title} - {self.address}"

class StoreGalleryModel(models.Model):
    """Represents gallery images for a store."""
    store = models.ForeignKey(
        StoreAddressModel, 
        on_delete=models.CASCADE, 
        related_name='gallery_images'
    )  # Each image is linked to a specific store
    images = models.JSONField()  # Stores a list of image paths
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional gallery description
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gallery for {self.store.store_name}"
    
class HomePageContentModel(models.Model):
    """Stores content for the homepage carousel sections."""
    title = models.CharField(max_length=255)  # Section title, e.g., 'Our Vision'
    content = models.TextField()  # Detailed description/content
    is_active = models.BooleanField(default=True)  # To toggle visibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FooterContentModel(models.Model):
    """Model to store title and description for footer sections."""
    title = models.CharField(max_length=255)  # Footer section title
    description = models.TextField()  # Footer section description
    is_active = models.BooleanField(default=True)  # For toggling visibility
    created_at = models.DateTimeField(auto_now_add=True)  # Record creation time
    updated_at = models.DateTimeField(auto_now=True)  # Record update time

    def __str__(self):
        return self.title