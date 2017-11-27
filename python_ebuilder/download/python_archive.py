from urllib.request import urlopen
from tempfile import NamedTemporaryFile, mkdtemp
import patoolib
import shutil
from contextlib import contextmanager
import os


@contextmanager
def get_setup_py(zipurl):
    # todo:zipurl is blank
    print("setup_url", zipurl)
    file_name = os.path.join("Downloads", zipurl.split('/')[-1])
    if os.path.exists(file_name):
        if os.path.getsize(file_name) == 0:
            print("size 0,removing...")
            os.remove(file_name)
        else:
            print("already in Downloads")
    if os.path.exists(file_name):
        pass
    else:
        print('downloading...')
        with urlopen(zipurl) as zipresp:
            with open(file_name, 'wb') as f:
                f.write(zipresp.read())

    with open(file_name, 'rb') as zipresp, NamedTemporaryFile() as tfile:
        tfile.write(zipresp.read())
        tfile.seek(0)
        tmpdir = mkdtemp()
        previousDir = os.getcwd()
        try:
            patoolib.extract_archive(tfile.name, outdir=tmpdir)

            for root, dirs, files in os.walk(tmpdir):
                if file_name.endswith('.whl'):
                    for file in files:
                        # and (os.path.dirname(root) == tmpdir or root == tmpdir)
                        if file == 'metadata.json' and (os.path.dirname(root) == tmpdir):
                            print(root, tmpdir)
                            fullPath = os.path.join(root, file)
                            os.chdir(root)
                            yield fullPath
                            break

                else:
                    for file in files:
                        if file == 'setup.py' and (os.path.dirname(root) == tmpdir or root == tmpdir):
                            fullPath = os.path.join(root, file)
                            os.chdir(root)
                            yield fullPath
                            break

        finally:
            os.chdir(previousDir)
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)


def main():
    zipurl = 'https://pypi.python.org/packages/23/2d/9790707eed08c802daee32183e7c98ec2e9797564dad229738b7f178e18e/howdoi-1.1.9.tar.gz'
    with get_setup_py(zipurl) as path:
        print(path)


if __name__ == '__main__':
    main()
