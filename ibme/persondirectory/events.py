from ibme.persondirectory.behaviors import IEntry


def directoryModifiedHandler(ob, event):
    """Reindex all content below when a directory is modified"""
    query = dict(object_provides=IEntry.__identifier__)
    for l in ob.restrictedTraverse('@@folderListing')(**query):
        l.getObject().reindexObject(idxs=["pdir_keywords"])
