import sys
import importlib
from pathlib import Path
import click

__author__ = 'tastu teche <tastuteche@yahoo.com>'
__description__ = 'Ebuild file producer for python  modules.'
__license__ = 'GNU General Public License v3 or later (GPLv3+)'
__version__ = '0.0.1'


# https://gist.github.com/vaultah/d63cb4c86be2774377aa674b009f759a


def import_parents(level=1):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:  # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__)  # won't be needed after that


if __name__ == '__main__' and __package__ is None:
    import_parents(level=1)


from .extract.pypi_page import get_data
from .extract.gentoo_host import add_host_info
from .transform.pypi_ebuild import process_data
from .transform.setup_py_ebuild import add_depend_info
from .generate.ebuild_file import render, render9999
from oslash.util.fn import compose


@click.command()
@click.argument('package_name')
@click.option('--version', default="", help='package version')
def main(package_name, version):
    # data = get_data('howdoi', 'sss)
    # options = process_data(data)
    # print(options)
    # render(options)
    print(package_name, version)
    comp = compose(render9999, add_depend_info, add_host_info,
                   process_data, get_data)

    result = comp(package_name, version)

    import os
    ebuild_dir = "portage/dev-python/%s" % package_name.replace('-', '_')
    if not os.path.exists(ebuild_dir):
        os.makedirs(ebuild_dir)
    ebuild_file = ebuild_dir + \
        "/%s-9999.ebuild" % package_name.replace('-', '_')
    with open(ebuild_file, 'w') as f:
        f.write(result)
    print(ebuild_file)


if __name__ == '__main__':
    main()
