# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.subsections.testing import COLLECTIVE_SUBSECTIONS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.subsections is properly installed."""

    layer = COLLECTIVE_SUBSECTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.subsections is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.subsections'))

    def test_uninstall(self):
        """Test if collective.subsections is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.subsections'])
        self.assertFalse(self.installer.isProductInstalled('collective.subsections'))

    def test_browserlayer(self):
        """Test that ICollectiveSubsectionsLayer is registered."""
        from collective.subsections.interfaces import ICollectiveSubsectionsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveSubsectionsLayer, utils.registered_layers())
