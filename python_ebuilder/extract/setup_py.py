import ast


def get_version(path):
    with open(path, 'rU') as file:
        t = compile(file.read(), path, 'exec', ast.PyCF_ONLY_AST)
        for node in (n for n in t.body if isinstance(n, ast.Expr)):

            if isinstance(node.value, ast.Call) and node.value.func.id == 'setup':
                for kw in node.value.keywords:
                    name = kw.arg

                    if name in ('__version__', '__version_info__', 'VERSION', 'version'):
                        v = kw.value
                        if isinstance(v, ast.Str):
                            version = v.s
                            return version
                        if isinstance(v, ast.Tuple):
                            r = []
                            for e in v.elts:
                                if isinstance(e, ast.Str):
                                    r.append(e.s)
                                elif isinstance(e, ast.Num):
                                    r.append(str(e.n))
                            version = '.'.join(r)
                            return version
    return ""


def main():
    path = '../test/setup.py'
    print(get_version(path))


if __name__ == '__main__':
    main()
