#from ..extract.setup_py_ast import get_data
from ..extract.setup_py_exec import import_and_extract
from ..download.python_archive import get_setup_py
import os
import re


def _filter(s):
    '''requests >=2.4.0'''
    return re.sub(r'[ ]?[>=<]+[0-9.]+$', r'', s)


def add_depend_info(options):
    if 'src_uri' in options:
        with get_setup_py(options['src_uri']) as path:
            thedir = os.path.dirname(path)
            #dic = get_data(path)
            dic = import_and_extract(thedir)
            if 'install_requires' in dic:
                options['rdepend'] = map(
                    lambda str: 'dev-python/' + _filter(str) + '[${PYTHON_USEDEP}]', dic['install_requires'])
            options['depend'] = ['dev-python/setuptools[${PYTHON_USEDEP}]']
            if 'license' in dic:
                options['license'] = dic['license']
    return options
