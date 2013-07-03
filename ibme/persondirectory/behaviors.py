from zope import schema
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.autoform import interfaces
from plone.supermodel import model

from ibme.persondirectory import _


class IDirectory(model.Schema):
    """The directory itself"""
    sorting = schema.Choice(
        title=_(u'Sorting of results'),
        description=_(u'Choose how you want the results sorted') +
        '(TODO: You need to re-index sortable_index manually)',
        required=True,
        default='title',
        vocabulary=SimpleVocabulary([
            SimpleTerm(value='title', title=_(u'By title, alphabetically')),
            SimpleTerm(value='surname', title=_(u'By title, name order')),
        ]),
    )
alsoProvides(IDirectory, interfaces.IFormFieldProvider)


class IEntry(model.Schema):
    """An entry within the directory"""
alsoProvides(IEntry, interfaces.IFormFieldProvider)
