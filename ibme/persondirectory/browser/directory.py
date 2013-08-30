from urllib import urlencode

from zope.component import getUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.Five import BrowserView

from ibme.persondirectory.behaviors import IEntry
from ibme.persondirectory.catalog import uniqueValues, fieldToFilter


class DirectoryView(BrowserView):
    """Class for all directory views"""
    def entryListing(self):
        """Get all entries for this view"""
        query = dict(
            sort_on='sortable_title',
            sort_order='ascending',
            object_provides=IEntry.__identifier__)

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

    def _getFilterFields(self):
        """Get all fields (and titles) that use the SuggestionFieldWidget"""
        if getattr(self, 'filter_fields', None) is None:
            fti = getUtility(IDexterityFTI, name='pdir_entry')
            schema = fti.lookupSchema()
            self.filter_fields = [
                (n, schema[n].title)
                for n
                in self.context.filter_fields
            ]
        return self.filter_fields

    def getFilters(self):
        """
        Return a deep structure of the form
            [
                dict(title='Filter 1', id='f1' values=[
                    dict(title='Value 1', uri='?f1=v1', selected=True),
                    dict(title='Value 2', uri='?f1=v2', selected=False),
                ]),
            ]
        """
        portal_catalog = self.context.portal_catalog

        def filterValues(name):
            """Return all values for each filter"""
            urlBase = self.context.absolute_url() + '?'
            return [dict(
                title=val,
                url=urlBase + urlencode({name: val}),
                selected=(self.request.get(name, None) == val),
            ) for val in sorted(uniqueValues(portal_catalog, name))]

        # Get filters, sorted by title
        return sorted([
            dict(id=name, title=title, values=filterValues(name))
            for (name, title)
            in self._getFilterFields()
        ], key=lambda k: k['title'])


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
