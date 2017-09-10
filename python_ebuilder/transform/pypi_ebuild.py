import datetime
import re


licenses = {
    "Academic Free License (AFL)": "AFL-3.0",
    "Aladdin Free Public License (AFPL)": "Aladdin",
    "Apache Software License": "Apache-2.0",
    "Artistic License": "Artistic",
    "BSD License": "BSD",
    "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication": "CC0-1.0",
    "Common Public License": "CPL-1.0",
    "GNU Affero General Public License v3": "AGPL-3",
    "GNU Affero General Public License v3 or later (AGPLv3+)": "AGPL-3",
    "GNU Free Documentation License (FDL)": "FDL-1.1+",
    "GNU General Public License (GPL)": "GPL-1+",
    "GNU General Public License v2 (GPLv2)": "GPL-2",
    "GNU General Public License v2 or later (GPLv2+)": "GPL-2+",
    "GNU General Public License v3 (GPLv3)": "GPL-3",
    "GNU General Public License v3 or later (GPLv3+)": "GPL-3+",
    "GNU Lesser General Public License v2 (LGPLv2)": "LGPL-2",
    "GNU Lesser General Public License v2 or later (LGPLv2+)": "LGPL-2+",
    "GNU Lesser General Public License v3 (LGPLv3)": "LGPL-3",
    "GNU Lesser General Public License v3 or later (LGPLv3+)": "LGPL-3+",
    "GNU Library or Lesser General Public License (LGPL)": "LGPL-2+",
    "ISC License (ISCL)": "ISC",
    "MIT License": "MIT",
    "Mozilla Public License 1.0 (MPL)": "MPL-1.0",
    "Mozilla Public License 1.1 (MPL 1.1)": "MPL-1.1",
    "Mozilla Public License 2.0 (MPL 2.0)": "MPL-2.0",
    "Public Domain": "public-domain",
    "Python License (CNRI Python License)": "CNRI",
    "Python Software Foundation License": "PYTHON",
    "Repoze Public License": "repoze",
    "W3C License": "W3C",
    "Zope Public License": "ZPL",
    "zlib/libpng License": "ZLIB"
}


def convert(value):
    result = value
    if value in licenses:
        result = licenses[value]
    return result


def get_python_compat(pkg_data):
    if "info" in pkg_data:
        info = pkg_data["info"]
    else:
        info = None

    categories = {}
    if info:
        if "Categories" in info:
            categories = info["Categories"]

    py_versions = []
    if 'Programming Language' in categories:
        for entry in categories['Programming Language']:
            if entry == '2':
                py_versions.extend(['2_7'])
            elif entry == '3':
                py_versions.extend(['3_3', '3_4', '3_5'])
            elif entry == '2.6':
                py_versions.extend(['2_7'])
            elif entry == '2.7':
                py_versions.extend(['2_7'])
            elif entry == '3.2':
                py_versions.extend(['3_3'])
            elif entry == '3.3':
                py_versions.extend(['3_3'])
            elif entry == '3.4':
                py_versions.extend(['3_4'])
            elif entry == '3.5':
                py_versions.extend(['3_5'])

    if not py_versions:
        py_versions = ['2_7', '3_3', '3_4', '3_5']
    py_versions = sorted(list(set(py_versions)))
    if len(py_versions) == 1:
        python_compat = '( python' + py_versions[0] + ' )'
    else:
        python_compat = '( python{' + py_versions[0]
        for ver in py_versions[1:]:
            python_compat += ',' + ver
        python_compat += '} )'

    return python_compat


def get_pkg_license(pkg_data):
    if "info" in pkg_data:
        info = pkg_data["info"]
    else:
        info = None

    pkg_license = ""
    if info:
        categories = {}
        if "Categories" in info:
            categories = info["Categories"]

            if "License" in categories:
                pkg_license = categories["License"][-1]

    pkg_license = convert(pkg_license)

    return pkg_license


def get_homepage(pkg_data):
    if "info" in pkg_data:
        info = pkg_data["info"]
    else:
        info = None

    homepage = ""
    if info:
        if "Home Page:" in info:
            homepage = info["Home Page:"]
    return homepage


def get_description(data):
    description = ""
    allowed_ords_desc = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
        set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                          ['+', '_', '-', ' ', '.', '(', ')', '[', ']', '{', '}', ','])))
    if 'index' in data:
        description = data['index']['description']

    description = "".join(
        [x for x in description if ord(x) in allowed_ords_desc])
    return description


def get_filtered_package(package):

    # todo: write filter functions
    allowed_ords_pkg = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
        set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                          ['+', '_', '-'])))
    filtered_package = "".join(
        [x for x in package if ord(x) in allowed_ords_pkg])
    return filtered_package


def get_filtered_version(version):
    now = datetime.datetime.now()
    pseudoversion = "%04d%02d%02d" % (now.year, now.month, now.day)
    filtered_version = version
    match_object = re.match("(^[0-9]+[a-z]?$)|(^[0-9][0-9\.]+[0-9][a-z]?$)",
                            filtered_version)
    if not match_object:
        filtered_version = pseudoversion

    return filtered_version


def get_src_uri(data):
    files_src_uri = ""
    source_uri = ""

    pkg_data = data
    if pkg_data["files"]:
        for file_entry in pkg_data["files"]:
            if file_entry["type"] == "\n    Source\n  ":
                files_src_uri = file_entry["url"]
                break

    if "info" in pkg_data:
        info = pkg_data["info"]
        download_url = ""
        if info:
            if "Download URL:" in info:
                download_url = info["Download URL:"]

        if download_url:
            source_uri = download_url  # todo: find how to define src_uri
        else:
            source_uri = files_src_uri

    return source_uri


def get_md5(data):
    md5 = ""

    pkg_data = data
    if pkg_data["files"]:
        for file_entry in pkg_data["files"]:
            if file_entry["type"] == "\n    Source\n  ":
                md5 = file_entry["md5"]
                break

    return md5


def process_data(data):
    """
    Process parsed package data.
    """
    ebuild_data = {}
    category = "dev-python"

    if 'index' in data:
        (package, version) = data['index']['name_version']
        pkg = package + "-" + version

        ebuild_data = {}
        ebuild_data["realname"] = package
        ebuild_data["realversion"] = version
        #filtered_package, filtered_version

        description = get_description(data)
        ebuild_data["description"] = description
        ebuild_data["longdescription"] = description

        ebuild_data["homepage"] = get_homepage(data)
        ebuild_data["license"] = get_pkg_license(data)
        ebuild_data["src_uri"] = get_src_uri(data)
        ebuild_data["md5"] = get_md5(data)
        ebuild_data["python_compat"] = get_python_compat(data)

        return ebuild_data
