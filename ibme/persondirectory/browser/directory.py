from urllib import urlencode

from zope.component import getUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.Five import BrowserView

from ibme.persondirectory.catalog import uniqueValues

WIDGET_NAME = 'ibme.persondirectory.widget.SuggestionFieldWidget'


class DirectoryView(BrowserView):
    """Class for all directory views"""
    def personListing(self):
        """Get all person objects for this view"""
        query = dict(portal_type='pdir_person')

        # Add any filters specified on the querystring
        for (name, title) in self.getFilterFields():
            if name in self.request:
                query[name] = self.request[name]

        return self.context.restrictedTraverse('@@folderListing')(**query)

    def uniqueFilterEntries(self):
        """Return a dict of unique entries for each filter"""
        out = dict()
        portal_catalog = self.context.portal_catalog

        for (name, title) in self.getFilterFields():
            out[name] = uniqueValues(portal_catalog, name)
        return out

    def getPersonFieldTitle(self, id):
        """Return the person field's title"""
        for (name, title) in self.getFilterFields():
            if name == id:
                return title
        raise ValueError(id)

    def getFilterFields(self):
        """Get all fields (and titles) that use the SuggestionFieldWidget"""
        if getattr(self, 'filter_fields', None) is None:
            fti = getUtility(IDexterityFTI, name='pdir_person')
            schema = fti.lookupSchema()
            tags = schema.getTaggedValue(u'plone.autoform.widgets')
            self.filter_fields = [(k, schema[k].title) for (k, v)
                                  in tags.items()
                                  if v == WIDGET_NAME]
        return self.filter_fields

    def generateFilterUrl(self, filter, value):
        """Return a URL with filter params added"""
        return self.context.absolute_url() + '?' + urlencode({filter: value})


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
