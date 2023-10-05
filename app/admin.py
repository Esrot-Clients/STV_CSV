from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import *

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'num_seats', 'is_active', 'created_at', 'last_modified_at')
    search_fields = ('campaign_name',)
    list_filter = ('is_active',)

    def export_campaigns_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="campaigns.csv"'

        writer = csv.writer(response)
        writer.writerow(['Campaign Name', 'Number of Seats', 'Is Active', 'Created At', 'Last Modified At'])

        for campaign in queryset:
            writer.writerow([campaign.campaign_name, campaign.num_seats, campaign.is_active, campaign.created_at, campaign.last_modified_at])

        return response

    export_campaigns_to_csv.short_description = "Export selected campaigns to CSV"

    actions = [export_campaigns_to_csv]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'preference', 'is_active', 'created_at', 'last_modified_at')
    list_filter = ('campaign_name__campaign_name', 'is_active')

    def export_votes_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="votes.csv"'

        writer = csv.writer(response)
        writer.writerow(['Campaign Name', 'Preference', 'Is Active', 'Created At', 'Last Modified At'])

        for vote in queryset:
            writer.writerow([vote.campaign_name.campaign_name, vote.preference, vote.is_active, vote.created_at, vote.last_modified_at])

        return response

    export_votes_to_csv.short_description = "Export selected votes to CSV"

    actions = [export_votes_to_csv]