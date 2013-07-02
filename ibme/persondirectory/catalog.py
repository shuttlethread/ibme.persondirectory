import re

from zope.component import getUtility

from plone.dexterity.interfaces import IDexterityFTI
from plone.indexer.decorator import indexer

from ibme.persondirectory.behaviors import IPerson

WIDGET_NAME = 'ibme.persondirectory.widget.SuggestionFieldWidget'


@indexer(IPerson)
def index_pdir_keywords_IPerson(object, **kw):
    """Crush all filter fields down to keywords"""
    out = []
    for (name, title) in getFilterFields():
        if getattr(object, name, None):
            out.append("%s:%s" % (name, getattr(object, name)))
    return out


@indexer(IPerson)
def index_sortable_title_IPerson(object, **kw):
    """Swap surname and firstname"""
    if object.__parent__.sorting == 'surname':
        # Assume title is a name, pull last word (surname) off and put it at
        # the start
        m = re.search('(.*) (.*)', object.title)
        if m:
            return " ".join(m.groups()[::-1])
    # Sort by title
    return object.title


def uniqueValues(portal_catalog, index):
    """Return the unique values for an index, creating it if necessary"""
    # If the index doesn't exist, create it and return nothing, as there can't
    # be any content yet
    if 'pdir_keywords' not in portal_catalog.Indexes:
        portal_catalog.addIndex('pdir_keywords', 'KeywordIndex')
        return []

    out = []
    for v in portal_catalog.Indexes['pdir_keywords'].uniqueValues():
        if not v.startswith(index + ':'):
            continue
        out.append(v.replace(index + ':', '', 1))
    return out


def fieldToFilter(fields):
    """Turn field request into a filter"""
    if len(fields) == 0:
        return dict()
    return dict(
        pdir_keywords=dict(
            query=["%s:%s" % (k, v) for (k, v) in fields.items()],
            operator="and",
        )
    )


def getFilterFields():
    """Fetch all fields that use SuggestionFieldWidget"""
    fti = getUtility(IDexterityFTI, name='pdir_entry')
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
