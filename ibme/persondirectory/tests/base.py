import unittest

from zope.component import getUtility

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import applyProfile
from plone.dexterity.interfaces import IDexterityFTI
from zope.configuration import xmlconfig


class DirectoryFixture(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import ibme.persondirectory
        xmlconfig.include(configurationContext, 'configure.zcml',
                          ibme.persondirectory)
        configurationContext.execute_actions()

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ibme.persondirectory:default')

    def tearDownPloneSite(self, portal):
        pass


FIXTURE = DirectoryFixture()

DIRECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="ibme.persondirectory:Integration")
DIRECTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="ibme.persondirectory:Functional")


class TestCase(unittest.TestCase):
    def setDefaultEntrySchema(self):
        """Switch back to default schema"""
        fti = getUtility(IDexterityFTI, name='pdir_entry')
        fti.manage_changeProperties(model_source=None)
        #NB: These aren't getting cleared by the above. Bug?
        fti.lookupSchema().setTaggedValue(u'plone.autoform.widgets', {})

    def setFullFatEntrySchema(self):
        """Switch schemas for one with lots of fields"""
        fti = getUtility(IDexterityFTI, name='pdir_entry')
        fti.manage_changeProperties(model_source="""
<model xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="title" type="zope.schema.TextLine">
      <description>Enter the person's name</description>
      <title>Name</title>
    </field>
    <field name="portrait" type="plone.namedfile.field.NamedBlobImage">
      <description>Upload an image of the user</description>
      <required>False</required>
      <title>The person's portrait</title>
    </field>
    <field name="position" type="zope.schema.TextLine">
      <description>Select the person's position'</description>
      <title>Position</title>
      <form:widget type="ibme.persondirectory.widget.SuggestionFieldWidget"/>
    </field>
    <field name="e_mail" type="zope.schema.TextLine">
      <description/>
      <title>E-mail address</title>
    </field>
    <field name="tel" type="zope.schema.TextLine">
      <description>Telephone number</description>
      <title>Tel</title>
    </field>
    <field name="research_group" type="zope.schema.TextLine">
      <description>Res</description>
      <title>Research Group</title>
      <form:widget type="ibme.persondirectory.widget.SuggestionFieldWidget"/>
    </field>
    <field name="affiliation" type="zope.schema.Set"
           form:widget="z3c.form.browser.checkbox.CheckBoxFieldWidget">
      <title>Affiliation</title>
      <value_type type="zope.schema.Choice">
        <values>
          <element>Red</element>
          <element>Green</element>
          <element>Blue</element>
          <element>Violet</element>
        </values>
      </value_type>
    </field>
  </schema>
</model>
        """)


class IntegrationTestCase(TestCase):
    layer = DIRECTORY_INTEGRATION_TESTING


class FunctionalTestCase(TestCase):
    layer = DIRECTORY_FUNCTIONAL_TESTING
