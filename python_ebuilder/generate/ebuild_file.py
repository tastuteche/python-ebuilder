from jinja2 import Environment, PackageLoader
import re


EBUILD_TEMPLATE_PACKAGE = 'python_ebuilder'
EBUILD_TEMPLATE = 'ebuild.jinja'
EBUILD_TEMPLATE_9999 = 'ebuild9999.jinja'

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


def _render(options, template_file):
    config = ConfigManager(options)
    template = env.get_template(template_file)

    output = template.render(options=config)
    output = output.replace('    ', '\t')
    return output


def render(options):
    return _render(options, EBUILD_TEMPLATE)


def render9999(options):
    return _render(options, EBUILD_TEMPLATE_9999)
