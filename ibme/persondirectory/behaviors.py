from zope.interface import alsoProvides

from plone.autoform import interfaces
from plone.supermodel import model


class IPersonDirectory(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IPersonDirectory, interfaces.IFormFieldProvider)


class IPerson(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IPerson, interfaces.IFormFieldProvider)
