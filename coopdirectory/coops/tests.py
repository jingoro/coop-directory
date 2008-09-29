from django.test import TestCase
from coops.models import Coop, CoopUser, CoopPicture, Contactable, AnsweredQuestion

from django.db import IntegrityError

class CoopRevisionTest(TestCase):
    fixtures = ['test_coops.json']

    def setUp(self):
        pass

    def testCoopRevisions(self):
        """
        Test the saving mechanism for "Coop" which maintains revisions.
        """

        # Set up a Coop to work with
        c = Coop()
        c.name = "Testy Coop"
        c.created_by = CoopUser.objects.all()[0]
        c.picture = CoopPicture.objects.all()[0]
        c.contactable = Contactable.objects.all()[0]
        c.save()

        # Make sure it saved right
        orig_id = c.id
        self.assertEquals(c.branch.id, orig_id)
        self.assertEquals(c.revision, 0)

        # Try making a revision
        c.name = "Testy Coop Revised"
        c.save()
        self.assertEquals(c.revision, 1)
        self.assertEquals(c.id, orig_id)
        self.assertEquals(c.branch.id, orig_id)
        old_version = Coop.objects.get(name = "Testy Coop")
        self.assertEquals(old_version.id, orig_id + 1)
        self.assertEquals(old_version.revision, c.revision - 1)

        # Make sure the old version copied right
        old_revisions = Coop.objects.filter(name = "Testy Coop")
        self.failUnless(len(old_revisions) > 0)
        old_revision = old_revisions[0]
        self.assertEqual(old_revision.branch, c.branch)
        self.assertNotEqual(old_revision.id, c.id)

        # Make sure you can't duplicate revision numbers
        bad = Coop()
        bad.name = "Bad"
        bad.created_by = CoopUser.objects.all()[0]
        bad.contactable = Contactable.objects.all()[0]
        bad.branch = c
        bad.revision = 0
        self.assertRaises(IntegrityError, bad.save)

        # Make sure revision of an old version pops out on top.  If we try to
        # edit an old revision, it should become the latest revision when
        # saved.
        all_revisions = Coop.objects.filter(branch__id = orig_id)
        latest = all_revisions[len(all_revisions) - 1]
        fork = all_revisions[0]
        self.assertEquals(fork.revision, 0)
        fork.name = "Testy Coop fork from old rev."
        fork.save()
        self.assertEqual(fork.revision, latest.revision + 1)
