import zope.interface
import zope.schema

from z3c.form.interfaces import IFormLayer, IFieldWidget, ITextWidget, NOVALUE
from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget

from ibme.persondirectory import _
from ibme.persondirectory.catalog import uniqueValues


class ISuggestionWidget(ITextWidget):
    """Interface: Text widget with suggestions"""


@zope.interface.implementer_only(ISuggestionWidget)
class SuggestionWidget(TextWidget):
    """Implementation: Text widget with suggestions"""
    klass = u'suggestion-widget'
    css = u'text'
    value = u''
    noValueToken = '--NOVALUE--'

    def items(self):
        """Return a list of suggestions the widget should make"""
        portal_catalog = self.context.portal_catalog
        items = [dict(value=self.noValueToken, selected=False,
                 content=_('Select an existing value...'))]

        for v in uniqueValues(portal_catalog, self.__name__):
            items.append(dict(content=v, selected=(v == self.value)))

        return items

    def extract(self, default=NOVALUE):
        """Extract the form value, text box wins over select box"""
        selectVal = self.request.get(self.name + '-datalist', default)
        textVal = self.request.get(self.name, default)
        return textVal if textVal != default else selectVal


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(IFieldWidget)
def SuggestionFieldWidget(field, request):
    """Factory: Text widget with suggestions"""
    return FieldWidget(field, SuggestionWidget(request))
