from django.db import models

# Create your models here.


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=100, verbose_name="Campaign Name")
    candidates = models.TextField(verbose_name="Candidates List", help_text="Enter candidates separated by commas")
    num_seats = models.PositiveIntegerField(verbose_name="Number of Seats")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    last_modified_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.campaign_name
    
    def save(self, *args, **kwargs):
        # Convert candidates' names to lowercase
        self.candidates = self.candidates.lower()
        # Remove leading and trailing spaces from candidates' names
        self.candidates = self.candidates.strip()
        super().save(*args, **kwargs)

    def delete(self):
        # Set is_active to False for soft deletion
        self.is_active = False
        self.save()



class Vote(models.Model):
    campaign_name = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Campaign")
    preference = models.TextField(verbose_name="Preference", help_text="Enter candidates separated by commas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    last_modified_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"Vote for {self.preference} in {self.campaign_name}"
    
    def delete(self):
        # Set is_active to False for soft deletion
        self.is_active = False
        self.save()