import re

from plone.indexer.decorator import indexer

from ibme.persondirectory.behaviors import IEntry

WIDGET_NAME = 'ibme.persondirectory.widget.SuggestionFieldWidget'


@indexer(IEntry)
def index_pdir_keywords_IEntry(object, **kw):
    """Crush all filter fields down to keywords"""
    out = []
    for name in object.aq_parent.filter_fields:
        if getattr(object, name, None) is None:
            continue
        elif hasattr(getattr(object, name), "__iter__"):
            for v in getattr(object, name):
                out.append("%s:%s" % (name, v))
        else:
            out.append("%s:%s" % (name, getattr(object, name)))
    return out


@indexer(IEntry)
def index_sortable_title_IEntry(object, **kw):
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
