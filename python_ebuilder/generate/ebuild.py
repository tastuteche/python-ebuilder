from jinja2 import Environment, PackageLoader
import re

EBUILD_TEMPLATE_PACKAGE = 'python_ebuilder'
EBUILD_TEMPLATE = 'ebuild.jinja'

env = Environment(
    loader=PackageLoader(EBUILD_TEMPLATE_PACKAGE, 'templates'),
    trim_blocks=True)


class ConfigManager(object):

    def __init__(self, configs={}):
        self.configs = configs

    def __repr__(self):
        return "<ConfigManager configs(%s)" % (list(self.configs.keys()))

    def __getattr__(self, name):
        return self.configs[name]


def replace_re(s, find, replace):
    return re.sub(find, replace, s)


env.filters['replace_re'] = replace_re


def render(options):
    template = env.get_template(EBUILD_TEMPLATE)

    output = template.render(options=options)
    output = output.replace('    ', '\t')
    print(output)
