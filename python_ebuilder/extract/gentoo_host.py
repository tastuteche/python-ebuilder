from portage import config as portage_config
from portage import settings as portage_settings
CONFIG = portage_config(clone=portage_settings)
ENV = CONFIG.environ()


def get_keyword():
    """Return ARCH from portage environment or None
    """
    arch = ENV.get('ARCH', None)

    if arch and not arch.startswith('~'):
        arch = "~%s" % arch
    return arch


# print(get_keyword())

from datetime import date
from ..__init__ import __version__


def add_host_info(options):
    options['gentoo_keywords'] = get_keyword()

    options["maintainer"] = [{'email': 'tastuteche@yahoo.com',
                              'name': 'Tastu Teche'}]

    options['python_modname'] = None
    options['rdepend'] = set()
    options['depend'] = set()
    options['use'] = set()
    options['warnings'] = set()
    options['slot'] = '0'
    options['s'] = ''
    options['tests_method'] = ''
    options["inherit"] = ['distutils-r1', 'prefix']
    options['python_ebuilder_version'] = __version__
    options['year'] = date.today().year
    return options
