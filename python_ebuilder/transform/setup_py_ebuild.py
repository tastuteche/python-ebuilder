#from ..extract.setup_py_ast import get_data
from ..extract.setup_py_import import import_and_extract
from ..download.python_archive import get_setup_py
from ..transform.gentoo_pkg import query_gentoo_pkg
import os
import re
import json


def _filter(s):
    '''requests >=2.4.0'''
    ''''numpy >=1.9.0, <2.0.0'''
    s = s.replace('(', '').replace(')', '')
    return re.sub(r'[ ]?[>=<]+[ ]*[0-9.]+([ ]*,[ ]*[>=<]+[ ]*[0-9.]+)?$', r'', s)


def add_depend_info(options):
    if 'src_uri' in options:
        with get_setup_py(options['src_uri']) as path:
            if path.endswith('metadata.json'):
                with open(path, 'r') as f:
                    json_meta = json.loads(f.read())
                    dic = {}
                    dic['install_requires'] = json_meta['run_requires'][0]['requires']
            else:
                thedir = os.path.dirname(path)
                #dic = get_data(path)
                # gfortran: error: ./glmnet_py/GLMnet.f: No such file or directory
                # No such file or directory: 'README.md'
                dic = import_and_extract(thedir)
            if 'install_requires' in dic:
                print('install_requires', dic['install_requires'])
                install_requires = filter(
                    lambda x: x != None and x.strip() != '', dic['install_requires'])
                options['rdepend'] = map(
                    lambda str: query_gentoo_pkg(_filter(str)) + '[${PYTHON_USEDEP}]', install_requires)
                options['depend'] = ['dev-python/setuptools[${PYTHON_USEDEP}]']
            if 'license' in dic:
                options['license'] = dic['license']
    return options
