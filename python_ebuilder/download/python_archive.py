from urllib.request import urlopen
from tempfile import NamedTemporaryFile, mkdtemp
import patoolib
import shutil
from contextlib import contextmanager


@contextmanager
def get_setup_py(zipurl):
    with urlopen(zipurl) as zipresp, NamedTemporaryFile() as tfile:
        tfile.write(zipresp.read())
        tfile.seek(0)
        tmpdir = mkdtemp()
        try:
            patoolib.extract_archive(tfile.name, outdir=tmpdir)

            import os
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    if file == 'setup.py':
                        fullPath = os.path.join(root, file)
                        previousDir = os.getcwd()
                        os.chdir(root)
                        yield fullPath
                        os.chdir(previousDir)
        finally:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)


def main():
    zipurl = 'https://pypi.python.org/packages/23/2d/9790707eed08c802daee32183e7c98ec2e9797564dad229738b7f178e18e/howdoi-1.1.9.tar.gz'
    with get_setup_py(zipurl) as path:
        print(path)


if __name__ == '__main__':
    main()
