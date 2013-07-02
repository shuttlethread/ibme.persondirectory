from zope import schema
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.autoform import interfaces
from plone.supermodel import model

from ibme.persondirectory import _


class IPersonDirectory(model.Schema):
    """The top of a QnA form
    """
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
alsoProvides(IPersonDirectory, interfaces.IFormFieldProvider)


class IPerson(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IPerson, interfaces.IFormFieldProvider)
