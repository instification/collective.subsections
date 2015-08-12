# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.subsections


class CollectiveSubsectionsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.subsections)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.subsections:default')


COLLECTIVE_SUBSECTIONS_FIXTURE = CollectiveSubsectionsLayer()


COLLECTIVE_SUBSECTIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SUBSECTIONS_FIXTURE,),
    name='CollectiveSubsectionsLayer:IntegrationTesting'
)


COLLECTIVE_SUBSECTIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SUBSECTIONS_FIXTURE,),
    name='CollectiveSubsectionsLayer:FunctionalTesting'
)


COLLECTIVE_SUBSECTIONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SUBSECTIONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveSubsectionsLayer:AcceptanceTesting'
)
