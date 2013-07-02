from urllib import urlencode

from Products.Five import BrowserView

from ibme.persondirectory.catalog import uniqueValues, fieldToFilter, \
    getFilterFields


class DirectoryView(BrowserView):
    """Class for all directory views"""
    def personListing(self):
        """Get all person objects for this view"""
        query = dict(
            sort_on='sortable_title',
            sort_order='ascending',
            portal_type='pdir_person')

        # Add any filters specified on the querystring
        query.update(fieldToFilter(dict(
            (n, self.request[n])
            for (n, t) in self.getFilterFields()
            if n in self.request)))

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
            self.filter_fields = getFilterFields()
        return self.filter_fields

    def generateFilterUrl(self, filter, value):
        """Return a URL with filter params added"""
        return self.context.absolute_url() + '?' + urlencode({filter: value})


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
