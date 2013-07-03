from plone.app.testing import setRoles, login, TEST_USER_NAME, TEST_USER_ID

from .base import IntegrationTestCase


class ContentTypeTest(IntegrationTestCase):

    def test_creation(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Can create directories
        portal.invokeFactory(type_name="pdir_directory",
                             id="dir", title="UT Directory")
        item = portal['dir']
        self.assertEquals(item.title, "UT Directory")
        self.assertEquals(item.sorting, "title")

        # Cannot nest directories
        with self.assertRaisesRegexp(ValueError, 'pdir_directory'):
            portal['dir'].invokeFactory(type_name="pdir_directory", id="ent1")

        # Can only create entries within a directory
        with self.assertRaisesRegexp(ValueError, 'pdir_entry'):
            portal.invokeFactory(type_name="pdir_entry", id="ent1")

        portal['dir'].invokeFactory(type_name="pdir_entry",
                                    id="ent1", title="Entry 1")
        item = portal['dir']['ent1']
        self.assertEquals(item.title, "Entry 1")
        #TODO: self.assertTrue(hasattr(item, 'image'))
