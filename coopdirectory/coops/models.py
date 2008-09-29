from django.db import models
from django.contrib.auth.models import User

import datetime

#
# Coop Users
#
# We extend the standard Django user class because it's easier for now.
#

class CoopUser(models.Model):
    user = models.OneToOneField(User)
    contactable = models.OneToOneField('Contactable')

    def __unicode__(self):
        return u"<%s - %s>" % (self.user, self.contactable)

#
# Versioned model
#
# A model which subclasses VersionedModel will keep a revision history of all
# changes to instances.  The revision order is maintained by the 
# "revision" field (the latest is always the highest revision number).
#
# Revisions are grouped by the "branch" field, which is a reference to the 
# current revision.  Consequently, a related model which points to the "branch" 
# value will always reference the current revision.  Old revisions get a new
# primary key when a new revision is saved.
#
# Examples:
#    # Get all revisions for a model:
#    >>> VersionedModelSubclass.objects.filter(branch__pk = 3)
#    # Get the latest revision:
#    >>> VersionedModelSubclass.objects.filter(branch__pk = 3).latest()
#
# Each revision stores the date when it was created, as well as the CoopUser
# that created the revision.  The CoopUser field must be manually filled by
# the saving view, or it will default to the original creator.
class VersionedModel(models.Model):
    # We only need "created" fields; each revision is an "update", see
    # revision 1 for the "original" creator and date.
    created_by = models.ForeignKey('CoopUser')

    # Automatically handled fields
    created_at = models.DateTimeField(auto_now_add = True)
    # All versions of a particular thing share a branch.
    branch = models.ForeignKey('self', null=True, blank=True, 
            related_name='%(class)s_branch', help_text="handled automatically, don't change")
    revision = models.IntegerField(default = 0, blank = True, help_text="handled automatically, don't change")

    # Ensure safety of revisions by using "@transaction.commit_on_success"
    # decorator in views that call save.
    def save(self, *args, **kwargs):
        # if this is an update (aka this model's been saved before):
        if self.pk:
            # get a new copy of the latest from database, without unsaved modifications
            latest = self.__class__.objects.get(pk = self.branch.pk)

            # update the new version
            self.pk = latest.pk # must set explicitly in case we aren't editing latest
            self.revision = latest.revision + 1
            self.created_at = datetime.datetime.now()
            super(VersionedModel, self).save(*args, **kwargs)
            
            # force insert by blanking pk
            latest.pk = None
            # Save old version next -- must be saved after new version is done,
            # or will raise IntegrityError
            super(VersionedModel, latest).save(*args, **kwargs)
        else:
            # First we must establish an instance.
            super(VersionedModel, self).save(*args, **kwargs)
            # Next, we can set the branch to self.
            self.branch = self
            super(VersionedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        get_latest_by = ['revision']
        ordering = ['revision']
        unique_together = ['branch', 'revision']

#
# Customizable Questions
#
# A "Question" is the general form of a question.  This includes the prompt (the
# question itself), a category, an optional set of answers, and switches for
# allowing free text answers or multiple answers.
#
# AnsweredQuestion is a particular Coop's chosen answer to a Question, which
# is owned by the coop.  
#
# Only AnsweredQuestion's are versioned; revised Question's should be
# given a new instance instead.  That way, people don't suddenly find they
# answered a different question than they thought they did.
#
# No database distinction is made between "fixed" and "free text" answers.  It
# is up to the UI to enforce whether a provided answer is one of the options
# specified in the Question.


# A Question is the general form of a question which may subsequently be
# answered.  These can be offered as suggestions when a house begins to
# construct their questions and answers.  If "free_text_answer" is true, the UI
# should provide an opportunity for free text answers.
class Question(models.Model):
    prompt = models.ForeignKey('Prompt')
    answers = models.ManyToManyField('Answer', null=True,
            through='AnswerOrder')
    multiple_answers_ok = models.BooleanField()
    free_text_answer_ok = models.BooleanField()
    category = models.ForeignKey('QuestionCategory', null=True, blank=True)
    def __unicode__(self):
        return u"<%s: %s>" % (self.prompt, "%s..." % self.answers.all()[0])

# The "question" part of a question.
class Prompt(models.Model):
    prompt = models.CharField(max_length=250)
    def __unicode__(self):
        return self.prompt

# The "answer" part of an answer.
class Answer(models.Model):
    answer = models.TextField()
    def __unicode__(self):
        return self.answer[:50]

# A join table between Question and Answer which provides ordering.
class AnswerOrder(models.Model):
    question_template = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    order = models.IntegerField()
    class Meta:
        unique_together = ['question_template', 'order']
        ordering = ['order']

# A coop's response to a Question
class AnsweredQuestion(VersionedModel):
    question = models.ForeignKey('Question') 
    answers = models.ManyToManyField('Answer')
    # The order this response appears in a coop's description
    order = models.IntegerField()
    coop = models.ForeignKey('Coop')
    def __unicode__(self):
        return u"<%s: %s>" % (self.question, self.answers.all()[0])

# An organizing strategy for questions.
class QuestionCategory(models.Model):
    category = models.CharField(max_length=50)
    parent = models.ForeignKey('QuestionCategory', null=True, blank=True)
    def __unicode__(self):
        return self.category

#
# Contactable
# This provides contact information for both coops and individual users.
#

class Contactable(models.Model): 
    def __unicode__(self):
        parts_1 = [u"%s" % a for a in self.email_set.all()]
        parts_2 = [u"%s" % a for a in self.phonenumber_set.all()]
        return u", ".join(parts_1 + parts_2) or u"none provided"

# A label for a contact method, e.g. "Main", "Work", "Home", etc.
class Label(models.Model):
    label = models.CharField(max_length=15)
    rank = models.PositiveSmallIntegerField()
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.label

class EmailLabel(Label): pass

class PhoneNumberLabel(Label): pass

# Abstract contact method (to be subclassed by Email and PhoneNumber)
class ContactMethod(models.Model):
    contactable = models.ForeignKey(Contactable)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Email(ContactMethod):
    label = models.ForeignKey(EmailLabel)
    email = models.EmailField()
    def __unicode__(self):
        return u"%s: %s" % (self.label, self.email)

class PhoneNumber(ContactMethod):
    label = models.ForeignKey(PhoneNumberLabel)
    phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s: %s" % [self.label, self.phone_number]

#
# Coops
#
# All optional meta-information is stored in AnsweredQuestion instances.  For
# simplicity, required fields (e.g., name, picture) are stored in hard-coded
# fields.
#
# XXX TODO: We need to specify some way of ordering and organizing
# the answer sets.  As of now, it's just an unordered set.

class Coop(VersionedModel):
    # Required manual-entry fields
    name = models.CharField(max_length=200)
    picture = models.ForeignKey('CoopPicture')
    contactable = models.ForeignKey(Contactable)
    related_coops = models.ManyToManyField('Coop', null=True, 
            through='CoopRelationship', symmetrical=False)

    # Optional manual-entry fields
    categories = models.ManyToManyField('CoopCategory', null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('show_coop', [str(self.id)])

    def __unicode__(self):
        return self.name

class CoopCategory(models.Model):
    category = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.category

# Relationships between coops.
class RelationshipType(models.Model):
    type = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.type

class CoopRelationship(models.Model):
    from_coop = models.ForeignKey(Coop, related_name="from_relationships")
    to_coop = models.ForeignKey(Coop, related_name="to_relationships")
    relationship_type = models.ForeignKey('RelationshipType')
    def __unicode__(self):
        return u"<%s - %s - %s>" % (from_coop, relationship, to_coop)

class CoopPicture(models.Model):
    stock = models.BooleanField(default = False)
    picture = models.ImageField(upload_to = "uploads/coop_pictures/%Y/%m/")
    def __unicode__(self):
        return u"%s" % self.picture
