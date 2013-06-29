from Products.Five import BrowserView

class DirectoryView(BrowserView):
    """Class for all directory views"""
    def personListing(self):
        """Get all person objects for this view"""
        listing = self.context.restrictedTraverse('@@folderListing')(**dict(
            sort_order='descending',
        ))
        return [item for item in listing if item.isVisibleInNav()]

class UniqueEntriesView(BrowserView):
    """Get unique entries for the specified field"""
