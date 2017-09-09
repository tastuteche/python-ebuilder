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


from .generate.ebuild import ConfigManager, render


def main():
    options = {"src_uri": "https://pypi.python.org/packages/source/qqqqqq"
               ""
               }
    config = ConfigManager(options)

    render(config)


if __name__ == '__main__':
    main()
