from plone.app.testing import setRoles, login, TEST_USER_NAME, TEST_USER_ID

from .base import IntegrationTestCase


class ContentTypeTest(IntegrationTestCase):

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.setFullFatEntrySchema()
        portal.invokeFactory(
            type_name="pdir_directory",
            id="dir",
            title="UT Directory")
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent1",
            title=u'Damion Canterbruy-Zephraiah')
        portal['dir'].invokeFactory(
            type_name="pdir_entry",
            id="ent2",
            title=u'Alfred Dimpleby Zachery')
        self.view = portal.unrestrictedTraverse('dir/view')

    def fillFacetFields(self):
        """Fill facet fields with some data"""
        portal = self.layer['portal']

        portal['dir']['ent1'].position = "Desk"
        portal['dir']['ent1'].research_group = "Cat pictures"
        portal['dir']['ent1'].reindexObject()
        portal['dir']['ent2'].position = "Desk"
        portal['dir']['ent2'].research_group = "Twitter"
        portal['dir']['ent2'].reindexObject()

    def test_entryListing(self):
        """Main content listings"""
        portal = self.layer['portal']
        self.fillFacetFields()

        # Show everything by default
        self.assertEquals(
            [x.id for x in self.view.entryListing()],
            ['ent2', 'ent1'])

        # Sorting option is honoured
        portal['dir'].sorting = "surname"
        portal['dir']['ent1'].reindexObject()
        portal['dir']['ent2'].reindexObject()
        self.assertEquals(
            [x.id for x in self.view.entryListing()],
            ['ent1', 'ent2'])

        # Can filter too
        request = self.layer['request']
        request.set('research_group', 'Cat pictures')
        self.assertEquals(
            [x.id for x in self.view.entryListing()],
            ['ent1'])

    def test_getTitle(self):
        """Uses the facets specified in the querystring"""
        self.assertEquals(
            self.view.getTitle(),
            "UT Directory")

        request = self.layer['request']
        request.set('rowsooch_gerp', 'not a filter')
        request.set('position', 'Desk')
        self.assertEquals(
            self.view.getTitle(),
            "UT Directory: Desk")

    def test_getFacets(self):
        """Get the facets specified in the querystring"""
        request = self.layer['request']
        request.set('rowsooch_gerp', 'not a filter')
        request.set('position', 'Desk')
        self.assertEquals(
            self.view.getFacets(),
            dict(position="Desk"))

    def test_uniqueFilterEntries(self):
        """Used to populate facets"""
        self.assertEquals(
            self.view.uniqueFilterEntries(),
            {'position': [], 'research_group': []})

        self.fillFacetFields()
        self.assertEquals(
            self.view.uniqueFilterEntries(), dict(
                position=["Desk"],
                research_group=["Cat pictures", "Twitter"],
            ))

    def test_getEntryFieldTitle(self):
        """Get titles from field"""
        self.assertEquals(
            self.view.getEntryFieldTitle('position'),
            u'Position')
        self.assertEquals(
            self.view.getEntryFieldTitle('research_group'),
            u'Research Group')

    def test_generateFilterUrl(self):
        """Parameters should be encoded"""
        self.assertEquals(
            self.view.generateFilterUrl('camel', '2 humps please'),
            'http://nohost/plone/dir?camel=2+humps+please')
