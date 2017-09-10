import sys
import importlib
from pathlib import Path

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
from .generate.ebuild_file import render
from oslash.util.fn import compose


def main():
    # data = get_data('howdoi', 'sss)
    # options = process_data(data)
    # print(options)
    # render(options)
    comp = compose(render, add_host_info, process_data, get_data)

    comp('howdoi', '1.1.9')


if __name__ == '__main__':
    main()
