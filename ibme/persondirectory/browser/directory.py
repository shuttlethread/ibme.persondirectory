from urllib import urlencode

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.Five import BrowserView


class DirectoryView(BrowserView):
    """Class for all directory views"""
    def personListing(self):
        """Get all person objects for this view"""
        query = dict(portal_type='pdir_person')

        # Add any filters specified on the querystring
        for f in self.context.filter_fields:
            if f in self.request:
                query[f] = self.request[f]

        return self.context.restrictedTraverse('@@folderListing')(**query)

    def uniqueFilterEntries(self):
        """Return a dict of unique entries for each filter"""
        out = dict()
        portal_catalog = self.context.portal_catalog

        for f in self.context.filter_fields:
            out[f] = portal_catalog.Indexes[f].uniqueValues()
        return out

    def getPersonFieldTitle(self, id):
        """Return the person field's title"""
        return self.getPersonFieldVocab().getTerm(id).title

    def getPersonFieldVocab(self):
        """Return the person field name/title vocabulary"""
        if getattr(self, 'fieldVocab', None) is None:
            factory = getUtility(IVocabularyFactory,
                                 'ibme.persondirectory.personfieldsvocab')
            self.fieldVocab = factory(self.context)
        return self.fieldVocab

    def generateFilterUrl(self, filter, value):
        """Return a URL with filter params added"""
        return self.context.absolute_url() + '?' + urlencode({filter: value})


class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
