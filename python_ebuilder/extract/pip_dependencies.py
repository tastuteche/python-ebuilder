# https://github.com/sourcegraph/pydep

#./pip-dependencies.sh howdoi
str = """pyquery
pygments
requests
requests-cache
lxml>=2.1
cssselect>0.7.9
chardet<3.1.0,>=3.0.2
idna<2.7,>=2.5
urllib3<1.23,>=1.21.1
certifi>=2017.4.17
"""

import re
for s in str.splitlines():
    print(s)
    if ',' in s:
        s1, s2, _ = s.split(',')
    elif '>' in s or '=' in s or '<' in s:
        pass
