from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.layout.navigation.root import getNavigationRoot

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import get_url,get_id,get_view_url
from Products.CMFCore.interfaces import ISiteRoot, IFolderish
from plone.memoize.view import memoize

from zope.component import getMultiAdapter

import logging


log = logging.getLogger("iomedia.navdropdown")

class GlobalSubSectionsViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('subsections.pt')

    def update(self):
        GlobalSectionsViewlet.update(self)
        self.context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        self.current_url = self.context_state.current_base_url()

        for tab in self.portal_tabs:
            if tab['id']!='Members':
                tab['subtab']=self.getsubtab(self.context,tab)
            else:
                tab['subtab']=[]
    def getsubtab(self,context,tab):
        query={}
        result=[]
        portal_properties = getToolByName(context, 'portal_properties')
        portal_catalog = getToolByName(context, 'portal_catalog')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        site_properties = getattr(portal_properties, 'site_properties')

        rootPath=getNavigationRoot(context)
        xpath='/'.join([rootPath,tab['id']])
        if 'path' in tab:
            xpath=tab['path']
        query['path'] = {'query' : xpath, 'depth' : 1}

        query['portal_type'] = utils.typesToList(context)

        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute

            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', [])

        # Get ids not to list
        idsNotToList = navtree_properties.getProperty('idsNotToList', ())
        excludedIds = {}
        for id in idsNotToList:
            excludedIds[id]=1

        rawresult = portal_catalog.searchResults(**query)

        # now add the content to results
        for item in rawresult:
            if not (excludedIds.has_key(item.getId) or item.exclude_from_nav):
                id, item_url = get_view_url(item)
                data = {'name'      :  utils.pretty_title_or_id(context, item),
                        'id'         : item.getId,
                        'url'        : item_url,
                        'description': item.Description,
                        'current'    : '',
                        'path'       : item.getPath(),
                        }
                if self.current_url.startswith(item_url):
                    data['current']='selected'
                data['subtabs']=self.getsubtab(self.context,data)
                result.append(data)
        return result
