from django.contrib import admin
from coopdirectory.coops.models import *

# Coop users

admin.site.register(CoopUser)

# Coops and questions

admin.site.register(CoopCategory)

class CoopRelationshipInline(admin.TabularInline):
    model = CoopRelationship
    extra = 1
    fk_name = 'from_coop'

class AnsweredQuestionInline(admin.TabularInline):
    model = AnsweredQuestion
    extra = 2
    exclude = ['branch', 'revision', 'created_at']
    filter_horizontal = ['answers']

class CoopAdmin(admin.ModelAdmin):
    filter_horizontal = ['related_coops', 'categories']
    inlines = [AnsweredQuestionInline, CoopRelationshipInline]
    exclude = ['branch', 'revision', 'created_at']

admin.site.register(Coop, CoopAdmin)
admin.site.register(CoopPicture)

# Question templates

admin.site.register(Prompt)
admin.site.register(Answer)
admin.site.register(QuestionCategory)

class AnswerOrderInline(admin.TabularInline):
    model = AnswerOrder
    extra = 7 

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOrderInline]

admin.site.register(Question, QuestionAdmin)

# Contactables

class EmailInline(admin.TabularInline):
    model = Email
    extra = 2

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 2

class ContactableAdmin(admin.ModelAdmin):
    inlines = [EmailInline, PhoneNumberInline]

admin.site.register(Contactable, ContactableAdmin)

admin.site.register(EmailLabel)
admin.site.register(PhoneNumberLabel)
