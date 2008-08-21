# from django.db import db
# from django.db.db import permalink
# from django.contrib.auth.db import User
# 
# from django.core.files.storage import FileSystemStorage
# 
# from sorl.thumbnail.fields import ImageWithThumbnailsField

from appengine_django.models import BaseModel
from google.appengine.ext import db

class Coop(BaseModel):
    created = db.DateTimeProperty(required = True, auto_now_add = True)
    modified = db.DateTimeProperty(required = True, auto_now = True)
    # contacts = db.ManyToManyField(User, blank = True, null = True)

    name = db.StringProperty(required = True)
    address = db.PostalAddressProperty(required = True)
    phone = db.PhoneNumberProperty(required = False)
    email = db.EmailProperty()

    # number_of_residents = db.IntegerField(blank = True, null = True)
    # average_rent = db.CharField(max_length = 50, blank = True)
    # description = db.TextField(blank = True,
    #         help_text = 'Tell us about your coop, and what makes it special.')
    # founded = db.IntegerField(blank = True, null = True,
    #         help_text = 'When was your coop started?')
    # 
    # picture = ImageWithThumbnailsField(blank = True, null = True,
    #         upload_to = "uploads/coop_pictures/%Y/%m/", 
    #         thumbnail = {'size': (100, 100)},
    #         extra_thumbnails = {
    #             'large': {'size': (400, 400)},
    #         })

    # organization = db.ForeignKey('Organization', 
    #         blank = True, null = True, 
    #         help_text = 'Do you belong to a larger coop organization?  If not, leave blank.')
    # def get_absolute_url(self):
    #     return ('show_coop', [str(self.id)])
    # get_absolute_url = permalink(get_absolute_url)
    # 
    # def __unicode__(self):
    #     return self.name

# class Organization(db.Model):
#     name = db.CharField(max_length = 50)
#     description = db.TextField()
#     contacts = db.ManyToManyField(User, blank = True, null = True)
# 
#     def __unicode__(self):
#         return self.name
