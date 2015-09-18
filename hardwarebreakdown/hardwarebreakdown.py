from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class Memory(IPlugin):
    def plugin_type(self):
        return 'builtin'

    def show_widget(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to - front, bu_dashbaord and group_dashboard. If page is set to bu_dashboard, or$
        if page == 'front':
            t = loader.get_template('erikng/hardwarebreakdown/templates/hardwarebreakdown_front.html')
            if not machines:
                machines = Machine.objects.all()

        if page == 'bu_dashboard':
            t = loader.get_template('erikng/hardwarebreakdown/templates/hardwarebreakdown_id.html')
            if not machines:
                machines = utils.getBUmachines(theid)

        if page == 'group_dashboard':
            t = loader.get_template('erikng/hardwarebreakdown/templates/hardwarebreakdown_id.html')
            if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

        if machines:
            hardwarebd = machines.values('machine_model').annotate(count=Count('machine_model')).order_by()
        else:
            hardwarebd = []

        c = Context({
            'title': 'Hardware Breakdown',
            'data': hardwarebd,
            'theid': theid,
            'page': page
        })
        return t.render(c), 4

    def filter_machines(self, machines, data):
        # You will be passed a QuerySet of machines, you then need to perform some filtering based on the 'data' part of the url from the show_widget$

        machines = machines.filter(memory__exact=data)

        return machines, 'Model '+data
