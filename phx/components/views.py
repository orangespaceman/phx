import json
import os

from django.conf import settings
from django.views.generic import TemplateView


class ComponentsListView(TemplateView):
    template_name = 'components/components_list.html'

    def get_context_data(self, **kwargs):
        context = super(ComponentsListView, self).get_context_data(**kwargs)
        context['components'] = self.build_components_list()

        return context

    def build_components_list(self):
        groups = []
        group_path = os.path.join(settings.SITE_ROOT, 'templates/components/')
        group_dirs = self.get_directories(group_path)

        for group_dir in group_dirs:
            group = {'dir': group_dir}
            components_path = os.path.join(group_path, group_dir)
            group['components'] = self.get_components(components_path)
            if (len(group['components']) > 0):
                groups.insert(len(groups), group)

        return groups

    def get_directories(self, path):
        return [
            name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))
        ]

    def get_components(self, path):
        components = []
        component_dirs = self.get_directories(path)
        component_dirs.sort()
        for component_dir in component_dirs:
            demoPath = os.path.join(path, component_dir, 'demo/demo.html')
            if (os.path.exists(demoPath)):
                components.insert(len(components), component_dir)

        return components


class ComponentsDetailView(TemplateView):

    def get_template_names(self):
        return 'components/{group}/{component}/demo/demo.html'.format(
            **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComponentsDetailView, self).get_context_data(**kwargs)
        data_path = (
            '/templates/components/{group}/{component}/demo/demo.json').format(
                **self.kwargs)
        data_path = settings.SITE_ROOT + data_path
        with open(data_path, encoding='utf-8') as data_file:
            context['data'] = json.load(data_file)

        return context
