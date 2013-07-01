def uniqueValues(portal_catalog, index):
    """Return the unique values for an index, creating it if necessary"""
    # If the index doesn't exist, create it and return nothing, as there can't
    # be any content yet
    if index not in portal_catalog.Indexes:
        portal_catalog.addIndex(index, 'FieldIndex')
        return []

    # Return all non-empty items
    return [i for i in portal_catalog.Indexes[index].uniqueValues() if i]
