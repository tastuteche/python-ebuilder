import datetime
import re


def process_data(data):
    """
    Process parsed package data.
    """
    ebuild_data = {}
    category = "dev-python"

    common_data = {}
    common_data["eclasses"] = ['g-sorcery', 'gs-pypi']
    common_data["maintainer"] = [{'email': 'jauhien@gentoo.org',
                                  'name': 'Jauhien Piatlicki'}]
    common_data["dependencies"] = ""  # serializable_elist(separator="\n\t")

    # todo: write filter functions
    allowed_ords_pkg = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
        set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                          ['+', '_', '-'])))

    allowed_ords_desc = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
        set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                          ['+', '_', '-', ' ', '.', '(', ')', '[', ']', '{', '}', ','])))

    now = datetime.datetime.now()
    pseudoversion = "%04d%02d%02d" % (now.year, now.month, now.day)

    if 'index' in data:
        (package, version) = data['index']['name_version']
        description = data['index']['description']

        pkg = package + "-" + version

        pkg_data = data

        files_src_uri = ""
        md5 = ""
        if pkg_data["files"]:
            for file_entry in pkg_data["files"]:
                if file_entry["type"] == "\n    Source\n  ":
                    files_src_uri = file_entry["url"]
                    md5 = file_entry["md5"]
                    break

        download_url = ""
        info = pkg_data["info"]
        if info:
            if "Download URL:" in info:
                download_url = info["Download URL:"]

        if download_url:
            source_uri = download_url  # todo: find how to define src_uri
        else:
            source_uri = files_src_uri

        if not source_uri:
            pass

        homepage = ""
        pkg_license = ""
        py_versions = []
        if info:
            if "Home Page:" in info:
                homepage = info["Home Page:"]
            categories = {}
            if "Categories" in info:
                categories = info["Categories"]

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

                if "License" in categories:
                    pkg_license = categories["License"][-1]
        # pkg_license = self.convert(
        #    [common_config, config], "licenses", pkg_license)

        if not py_versions:
            py_versions = ['2_7', '3_3', '3_4', '3_5']

        if len(py_versions) == 1:
            python_compat = '( python' + py_versions[0] + ' )'
        else:
            python_compat = '( python{' + py_versions[0]
            for ver in py_versions[1:]:
                python_compat += ',' + ver
            python_compat += '} )'

        filtered_package = "".join(
            [x for x in package if ord(x) in allowed_ords_pkg])
        description = "".join(
            [x for x in description if ord(x) in allowed_ords_desc])
        filtered_version = version
        match_object = re.match("(^[0-9]+[a-z]?$)|(^[0-9][0-9\.]+[0-9][a-z]?$)",
                                filtered_version)
        if not match_object:
            filtered_version = pseudoversion

        ebuild_data = {}
        ebuild_data["realname"] = package
        ebuild_data["realversion"] = version

        ebuild_data["description"] = description
        ebuild_data["longdescription"] = description

        ebuild_data["homepage"] = homepage
        ebuild_data["license"] = pkg_license
        ebuild_data["src_uri"] = source_uri
        ebuild_data["md5"] = md5
        ebuild_data["python_compat"] = python_compat

        # pkg_db.add_package(
        #    Package(category, filtered_package, filtered_version), ebuild_data)
        return ebuild_data
