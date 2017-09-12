from ..extract.setup_py_ast import get_data
from ..download.python_archive import get_setup_py


def add_depend_info(options):
    if 'src_uri' in options:
        with get_setup_py(options['src_uri']) as path:
            dic = get_data(path)
            if 'install_requires' in dic:
                options['rdepend'] = map(
                    lambda str: 'dev-python/' + str + '[${PYTHON_USEDEP}]', dic['install_requires'])
            options['depend'] = ['dev-python/setuptools[${PYTHON_USEDEP}]']
            if 'license' in dic:
                options['license'] = dic['license']
    return options
