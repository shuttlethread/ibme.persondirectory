from zope import schema
from zope.component import getUtility
from zope.interface import implements, alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.autoform import interfaces
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import form
from plone.supermodel import model

from ibme.persondirectory import _


class IPersonDirectory(model.Schema):
    """The top of a QnA form
    """
    form.widget(filter_fields=CheckBoxFieldWidget)
    filter_fields = schema.List(
        title=_(u'Indexed person fields to filter'),
        description=_(u'Select which fields have a catalog FieldIndex set-up'),
        value_type=schema.Choice(
            vocabulary='ibme.persondirectory.personfieldsvocab'),
        default=[],
        required=False)

alsoProvides(IPersonDirectory, interfaces.IFormFieldProvider)


class PersonFieldsVocab(object):
    implements(IVocabularyFactory)
    """Make a vocabulary of all pdir_person fields
    """

    def __new__(self, context):
        """Fetch pdir_person's schema, and turn fields into vocab"""
        schema = getUtility(IDexterityFTI, name='pdir_person').lookupSchema()

        return SimpleVocabulary([
            SimpleVocabulary.createTerm(name, name, schema[name].title)
            for name in schema
        ])


class IPerson(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IPerson, interfaces.IFormFieldProvider)
