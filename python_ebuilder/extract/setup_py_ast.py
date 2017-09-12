import ast
from oslash.list import List
from collections import ChainMap
from functools import partial


def _get_setup_args(path):
    rtn = List.empty()
    with open(path, 'rU') as file:
        t = compile(file.read(), path, 'exec', ast.PyCF_ONLY_AST)
        for node in (n for n in t.body if isinstance(n, ast.Expr)):
            if isinstance(node.value, ast.Call) and node.value.func.id == 'setup':
                rtn = List.from_iterable(node.value.keywords)
                break

    return rtn


def _get_value(keyname, alias_list, kw):
    name = kw.arg
    rtn = {}

    def get_list_value(v):
        r = []
        for e in v.elts:
            if isinstance(e, ast.Str):
                r.append(e.s)
            elif isinstance(e, ast.Num):
                r.append(str(e.n))
        return r
    get_tuple_value = get_list_value

    if name in alias_list:
        v = kw.value
        if isinstance(v, ast.Str):
            rtn[keyname] = v.s
        elif isinstance(v, ast.Tuple):
            rtn[keyname] = get_tuple_value(v)
        elif isinstance(v, ast.List):
            rtn[keyname] = get_list_value(v)
        elif isinstance(v, ast.BinOp):
            if isinstance(v.left, ast.List):
                rtn[keyname] = get_list_value(v.left)
        else:
            #print(name, dir(v))
            pass

    return List.unit(rtn)


def get_data(setup_py_path):

    keydict = {"version": ('__version__', '__version_info__', 'VERSION', 'version'),
               "description": ('description'),
               "license": ('license'),
               "install_requires": ('install_requires'),
               }
    lstParser = map(lambda item: partial(
        _get_value, item[0], item[1]), keydict.items())

    setup_args = _get_setup_args(setup_py_path)

    def apply_parser(parser):
        lst = setup_args | parser
        parsed = dict(ChainMap(*lst))
        return parsed
    argList = map(apply_parser, lstParser)
    argDict = dict(ChainMap(*argList))
    return argDict


def main():
    path = '../test/setup.py'
    data = get_data(path)
    print(data)


if __name__ == '__main__':
    main()
