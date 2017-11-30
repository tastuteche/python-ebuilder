import sys
import mock
import setuptools
import tempfile
import os
import distutils.core
import re


def is_setuptools(content):
    return len(re.findall('from\s+setuptools\s+import.*(\s|,)setup', content)) > 0


def is_distutils(content):
    return len(re.findall('from\s+distutils\.core\s+import.*(\s|,)setup', content)) > 0


def import_and_extract(parent_dir):
    sys.path.insert(0, parent_dir)
    with tempfile.NamedTemporaryFile(prefix="setup_temp_", mode='w', dir=parent_dir, suffix='.py') as temp_fh:
        with open(os.path.join(parent_dir, "setup.py"), 'r') as setup_fh:
            content = setup_fh.read()
            temp_fh.write('\n\n'.join(["__name__ = '__main__'", content]))
            temp_fh.flush()
        try:
            if is_setuptools(content):
                with mock.patch.object(setuptools, 'setup') as mock_setup:
                    print('is_setuptools')
                    module_name = os.path.basename(temp_fh.name).split(".")[0]
                    setup_py_module = __import__(module_name)
            elif is_distutils(content):
                with mock.patch.object(distutils.core, 'setup') as mock_setup:
                    print('is_distutils')
                    module_name = os.path.basename(temp_fh.name).split(".")[0]
                    setup_py_module = __import__(module_name)
        finally:
            # need to blow away the pyc
            try:
                os.remove("%sc" % temp_fh.name)
            except:
                print(("Failed to remove %sc" % temp_fh.name), file=sys.stderr)
        if mock_setup.call_args is None:
            # https://github.com/mockfs/mockfs/blob/master/setup.py
            try:
                setup_py_module.main()
            except AttributeError:
                pass

        args, kwargs = mock_setup.call_args
        return kwargs


if __name__ == "__main__":
    if len(sys.argv) > 1:
        thedir = sys.argv[1]
        if not os.path.isdir(thedir):
            thedir = os.path.dirname(thedir)
        print(import_and_extract(thedir))
    else:
        print("syntax: %s directory" % sys.argv[0], file=sys.stderr)
