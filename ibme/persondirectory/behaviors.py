from zope import schema
from zope.component import getUtility
from zope.interface import implements, alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.autoform import interfaces
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import form
from plone.supermodel import model

from ibme.persondirectory import _


class IDirectory(model.Schema):
    """The directory itself"""
    filter_fields = schema.List(
        title=_(u'Fields to filter by'),
        description=_(u'Select which fields should be used as facets'),
        value_type=schema.Choice(
            vocabulary='ibme.persondirectory.entryfieldsvocab'),
        default=[],
        required=False)
    form.widget(filter_fields=CheckBoxFieldWidget)

    sorting = schema.Choice(
        title=_(u'Sorting of results'),
        description=_(u'Choose how you want the results sorted'),
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


class EntryFieldsVocab(object):
    implements(IVocabularyFactory)
    """Make a vocabulary of all pdir_entry fields
    """

    def __new__(self, context):
        """Fetch pdir_entry's schema, and turn fields into vocab"""
        schema = getUtility(IDexterityFTI, name='pdir_entry').lookupSchema()

        return SimpleVocabulary([
            SimpleVocabulary.createTerm(name, name, schema[name].title)
            for name in schema
        ])
