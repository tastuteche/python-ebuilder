import sys
import mock
import setuptools
import tempfile
import os


def import_and_extract(parent_dir):
    sys.path.insert(0, parent_dir)
    with tempfile.NamedTemporaryFile(prefix="setup_temp_", mode='w', dir=parent_dir, suffix='.py') as temp_fh:
        with open(os.path.join(parent_dir, "setup.py"), 'r') as setup_fh:
            temp_fh.write(setup_fh.read())
            temp_fh.flush()
        try:
            with mock.patch.object(setuptools, 'setup') as mock_setup:
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
