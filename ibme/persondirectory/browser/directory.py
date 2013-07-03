from urllib import urlencode

from Products.Five import BrowserView

from ibme.persondirectory.catalog import uniqueValues, fieldToFilter, \
    getFilterFields


class DirectoryView(BrowserView):
    """Class for all directory views"""
    def entryListing(self):
        """Get all entries for this view"""
        query = dict(
            sort_on='sortable_title',
            sort_order='ascending',
            portal_type='pdir_entry')

        # Add any filters specified on the querystring
        query.update(fieldToFilter(self.getFacets()))

        return self.context.restrictedTraverse('@@folderListing')(**query)

    def getTitle(self):
        """Return page title, with headings attached"""
        facets = ", ".join(self.getFacets().values())
        if len(facets) > 0:
            return self.context.title + ": " + facets
        else:
            return self.context.title

    def getFacets(self):
        """Get the asked-for facets"""
        return dict(
            (n, self.request[n])
            for (n, t) in self._getFilterFields()
            if n in self.request)

    def uniqueFilterEntries(self):
        """Return a dict of unique entries for each filter"""
        out = dict()
        portal_catalog = self.context.portal_catalog

        for (name, title) in self._getFilterFields():
            out[name] = uniqueValues(portal_catalog, name)
        return out

    def getEntryFieldTitle(self, id):
        """Return the title of the given field"""
        for (name, title) in self._getFilterFields():
            if name == id:
                return title
        raise ValueError(id)

    def _getFilterFields(self):
        """Get all fields (and titles) that use the SuggestionFieldWidget"""
        if getattr(self, 'filter_fields', None) is None:
            self.filter_fields = getFilterFields()
        return self.filter_fields

    def generateFilterUrl(self, filter, value):
        """Return a URL with filter params added"""
        return self.context.absolute_url() + '?' + urlencode({filter: value})


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
