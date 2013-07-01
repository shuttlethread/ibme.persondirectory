from urllib import urlencode

from zope.component import getUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.Five import BrowserView


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
            out[name] = portal_catalog.Indexes[name].uniqueValues()
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
            schema = getUtility(IDexterityFTI, name='pdir_person').lookupSchema()
            self.filter_fields = [(k, schema[k].title) for (k, v)
                in schema.getTaggedValue(u'plone.autoform.widgets').items()
                if v == 'ibme.persondirectory.widget.SuggestionFieldWidget']
        return self.filter_fields

    def generateFilterUrl(self, filter, value):
        """Return a URL with filter params added"""
        return self.context.absolute_url() + '?' + urlencode({filter: value})


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
