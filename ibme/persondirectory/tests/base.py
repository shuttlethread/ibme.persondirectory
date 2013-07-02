from unittest import TestCase

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, login, logout
from zope.configuration import xmlconfig

from Products.CMFCore.utils import getToolByName


class DirectoryFixture(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import ibme.persondirectory
        xmlconfig.include(configurationContext, 'configure.zcml', ibme.persondirectory)
        configurationContext.execute_actions()

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ibme.persondirectory:default')

    def tearDownPloneSite(self, portal):
        pass


FIXTURE = DirectoryFixture()

DIRECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="ibme.persondirectory:Integration",
    )
DIRECTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="ibme.persondirectory:Functional",
    )


class IntegrationTestCase(TestCase):
    layer = DIRECTORY_INTEGRATION_TESTING


class FunctionalTestCase(TestCase):
    layer = DIRECTORY_FUNCTIONAL_TESTING
