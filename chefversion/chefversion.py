from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count, F
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings


class ChefVersion(IPlugin):
    def widget_width(self):
        return 4

    def get_description(self):
        return 'Chef version'

    def widget_content(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('chefversion/templates/front.html')

        if page == 'bu_dashboard':
            t = loader.get_template('chefversion/templates/id.html')

        if page == 'group_dashboard':
            t = loader.get_template('chefversion/templates/id.html')

        try:
            chef_info = machines.filter(pluginscriptsubmission__plugin__exact='ChefVersion', pluginscriptsubmission__pluginscriptrow__pluginscript_name__exact='Version').annotate(chef_version=F('pluginscriptsubmission__pluginscriptrow__pluginscript_data')).values('chef_version').annotate(count=Count('chef_version')).order_by('chef_version')  # noqa: E501
        except Exception:
            chef_info = []

        c = Context({
            'title': 'Chef Version',
            'data': chef_info,
            'theid': theid,
            'page': page,
            'plugin': 'ChefVersion',
        })
        return t.render(c)

    def filter_machines(self, machines, data):
        machines = machines.filter(
            pluginscriptsubmission__plugin__exact='ChefVersion',
            pluginscriptsubmission__pluginscriptrow__pluginscript_name__exact='Version',
            pluginscriptsubmission__pluginscriptrow__pluginscript_data__exact=data)

        return machines, 'Machines with Chef version ' + data
