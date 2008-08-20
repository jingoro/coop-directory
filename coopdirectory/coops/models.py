from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage

from sorl.thumbnail.fields import ImageWithThumbnailsField

class Coop(models.Model):
    record_added = models.DateTimeField(auto_now_add = True, blank = True)
    record_modified = models.DateTimeField(auto_now = True, blank = True)
    contacts = models.ManyToManyField(User, blank = True, null = True)

    name = models.CharField(max_length = 50)
    street_address_1 = models.CharField(max_length = 50, blank = True)
    street_address_2 = models.CharField(max_length = 50, blank = True)
    city = models.CharField(max_length = 50, blank = True)
    state = models.USStateField(blank = True)
    zip_code = models.CharField(max_length = 10, blank = True)
    phone = models.CharField(max_length = 13, blank = True)
    public_email = models.EmailField(blank = True)

    number_of_residents = models.IntegerField(blank = True, null = True)
    average_rent = models.CharField(max_length = 50, blank = True)
    description = models.TextField(blank = True,
            help_text = 'Tell us about your coop, and what makes it special.')
    founded = models.IntegerField(blank = True, null = True,
            help_text = 'When was your coop started?')

    picture = ImageWithThumbnailsField(blank = True, null = True,
            upload_to = "uploads/coop_pictures/%Y/%m/", 
            thumbnail = {'size': (100, 100)},
            extra_thumbnails = {
                'large': {'size': (400, 400)},
            })

    organization = models.ForeignKey('Organization', 
            blank = True, null = True, 
            help_text = 'Do you belong to a larger coop organization?  If not, leave blank.')
    def get_absolute_url(self):
        return ('show_coop', [str(self.id)])
    get_absolute_url = permalink(get_absolute_url)

    def __unicode__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    contacts = models.ManyToManyField(User, blank = True, null = True)

    def __unicode__(self):
        return self.name
