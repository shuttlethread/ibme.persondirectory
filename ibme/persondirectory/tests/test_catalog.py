from Products.CMFCore.utils import getToolByName

from plone.app.testing import setRoles, login, TEST_USER_NAME, TEST_USER_ID

from .base import IntegrationTestCase

from ibme.persondirectory.catalog import fieldToFilter, \
    uniqueValues


class CatalogTest(IntegrationTestCase):

    def test_index_pdir_keywords_IEntry(self):
        """Make sure indexers do what we expect"""
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        def getMetadata(brain, name):
            return catalog.getIndexDataForRID(brain.getRID())[name]

        # Create a directory and some items
        portal.invokeFactory(type_name="pdir_directory",
                             id="dir", title="UT Directory")
        self.assertEquals(portal['dir'].sorting, "title")
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent1",
            title=u'Damion Canterbruy-Zephraiah')
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent2",
            title=u'Alfred Dimpleby Zachery')

        brains = catalog(portal_type="pdir_entry",
                         sort_on='sortable_title', sort_order='ascending')
        self.assertEquals(getMetadata(brains[0], 'sortable_title'),
                          u'Alfred Dimpleby Zachery')
        self.assertEquals(getMetadata(brains[1], 'sortable_title'),
                          u'Damion Canterbruy-Zephraiah')

        # Change sorting, should cause ordering to change
        portal['dir'].sorting = "surname"
        portal['dir']['ent1'].reindexObject()
        portal['dir']['ent2'].reindexObject()
        brains = catalog(portal_type="pdir_entry",
                         sort_on='sortable_title', sort_order='ascending')
        self.assertEquals(getMetadata(brains[0], 'sortable_title'),
                          u'Canterbruy-Zephraiah Damion')
        self.assertEquals(getMetadata(brains[1], 'sortable_title'),
                          u'Zachery Alfred Dimpleby')

    def test_fieldToFilter(self):
        self.assertEquals(
            fieldToFilter(dict(position="Butcher")),
            dict(pdir_keywords=dict(
                query=["position:Butcher"], operator="and"
            )))
        self.assertEquals(
            fieldToFilter(dict(position="Butcher", cut="Rump")),
            dict(pdir_keywords=dict(
                query=["position:Butcher", "cut:Rump"], operator="and"
            )))

    def test_uniqueValues(self):
        """Test index_pdir_keywords_IEntry will index keywords"""
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # No content, so no uniqe values
        self.assertEquals(uniqueValues(catalog, 'position'), [])
        self.assertEquals(uniqueValues(catalog, 'research_group'), [])
        self.assertEquals(uniqueValues(catalog, 'dont_exist'), [])

        # Create some entries, still no unique values yet
        self.setFullFatEntrySchema()
        portal.invokeFactory(
            type_name="pdir_directory",
            id="dir",
            title="UT Directory",
            filter_fields=['position', 'research_group', 'affiliation'],
        )
        self.assertEquals(portal['dir'].sorting, "title")
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent1",
            title=u'Damion Canterbruy-Zephraiah')
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent2",
            title=u'Alfred Dimpleby Zachery')
        self.assertEquals(uniqueValues(catalog, 'position'), [])
        self.assertEquals(uniqueValues(catalog, 'research_group'), [])
        self.assertEquals(uniqueValues(catalog, 'dont_exist'), [])

        # Enter values, should start appearing
        portal['dir']['ent1'].position = "Desk"
        portal['dir']['ent1'].research_group = "Cat pictures"
        portal['dir']['ent1'].affiliation = ["Red", "Violet"]
        portal['dir']['ent1'].reindexObject()
        portal['dir']['ent2'].position = "Desk"
        portal['dir']['ent2'].research_group = "Twitter"
        portal['dir']['ent2'].affiliation = ["Green", "Violet", "Blue"]
        portal['dir']['ent2'].reindexObject()
        self.assertEquals(
            uniqueValues(catalog, 'position'),
            ["Desk"])
        self.assertEquals(
            uniqueValues(catalog, 'research_group'),
            ["Cat pictures", "Twitter"])
        self.assertEquals(
            uniqueValues(catalog, 'affiliation'),
            ['Blue', 'Green', 'Red', 'Violet'])
        self.assertEquals(uniqueValues(catalog, 'dont_exist'), [])

        # Change again
        portal['dir']['ent2'].position = "Kitchen"
        portal['dir']['ent2'].research_group = "Cups of tea"
        portal['dir']['ent2'].reindexObject()
        self.assertEquals(
            uniqueValues(catalog, 'position'),
            ["Desk", "Kitchen"])
        self.assertEquals(
            uniqueValues(catalog, 'research_group'),
            ["Cat pictures", "Cups of tea"])
        self.assertEquals(uniqueValues(catalog, 'dont_exist'), [])
