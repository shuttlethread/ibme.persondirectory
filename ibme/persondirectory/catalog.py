from zope.component import getUtility

from plone.dexterity.interfaces import IDexterityFTI

WIDGET_NAME = 'ibme.persondirectory.widget.SuggestionFieldWidget'


def uniqueValues(portal_catalog, index):
    """Return the unique values for an index, creating it if necessary"""
    # If the index doesn't exist, create it and return nothing, as there can't
    # be any content yet
    if index not in portal_catalog.Indexes:
        portal_catalog.addIndex(index, 'FieldIndex')
        return []

    # Return all non-empty items
    return [i for i in portal_catalog.Indexes[index].uniqueValues() if i]


def fieldToFilter(fields):
    """Turn field request into a filter"""
    return fields


def getFilterFields():
    """Fetch all fields that use SuggestionFieldWidget"""
    fti = getUtility(IDexterityFTI, name='pdir_person')
    schema = fti.lookupSchema()
    tags = schema.getTaggedValue(u'plone.autoform.widgets')

    out = []
    for (k, v) in tags.items():
        if hasattr(v, 'getWidgetFactoryName'):
            # Widget is wrapped by ParameterizedWidget
            name = v.getWidgetFactoryName()
        else:
            name = v
        if name == WIDGET_NAME:
            out.append((k, schema[k].title,))
    return out
