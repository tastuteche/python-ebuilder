import urllib.request
from bs4 import BeautifulSoup
from oslash.list import List


def get_result(name, version):
    theurl = "https://pypi.python.org/pypi/%s" % name
    thepage = urllib.request.urlopen(theurl)
    soup = BeautifulSoup(thepage, "lxml")
    return List.unit(soup)


def get_index(soup):
    data = {}
    data["index"] = {}
    for div in soup("div", id="download-button"):
        lst = div.parent.find("h1").text.split()
        data["index"]['name_version'] = (lst[0], lst[1])
        data["index"]['description'] = div.parent.findNext('p').text
        data["index"]['download_url'] = div.find('a')["href"]
        break

    return List.unit(data)


def get_table(soup):
    data = {}
    data["files"] = []
    for table in soup("table", class_="list")[-1:]:
        if not "File" in table("th")[0].string:
            continue

        for entry in table("tr")[1:-1]:
            fields = entry("td")

            FILE = 0
            URL = 0
            MD5 = 1

            TYPE = 1
            PYVERSION = 2
            UPLOADED = 3
            SIZE = 4

            file_inf = fields[FILE]("a")[0]["href"].split("#")
            file_url = file_inf[URL]
            file_md5 = file_inf[MD5][4:]

            file_type = fields[TYPE].string
            file_pyversion = fields[PYVERSION].string
            file_uploaded = fields[UPLOADED].string
            file_size = fields[SIZE].string

            data["files"].append({"url": file_url,
                                  "md5": file_md5,
                                  "type": file_type,
                                  "pyversion": file_pyversion,
                                  "uploaded": file_uploaded,
                                  "size": file_size})
            entry.decompose()
        table.decompose()
    return List.unit(data)


def get_ul(soup):
    data = {}
    data["info"] = {}
    uls = soup("ul", class_="nodot")
    if uls:
        if "Downloads (All Versions):" in uls[0]("strong")[0].string:
            ul = uls[1]
        else:
            ul = uls[0]

        for entry in ul.contents:
            if not hasattr(entry, "name") or entry.name != "li":
                continue
            entry_name = entry("strong")[0].string
            if not entry_name:
                continue

            if entry_name == "Categories":
                data["info"][entry_name] = {}
                for cat_entry in entry("a"):
                    cat_data = cat_entry.string.split(" :: ")
                    if not cat_data[0] in data["info"][entry_name]:
                        data["info"][entry_name][cat_data[0]] = cat_data[1:]
                    else:
                        data["info"][entry_name][cat_data[0]].extend(
                            cat_data[1:])
                continue

            if entry("span"):
                data["info"][entry_name] = entry("span")[0].string
                continue

            if entry("a"):
                data["info"][entry_name] = entry("a")[0]["href"]
                continue
            entry.decompose()
        ul.decompose()
    return List.unit(data)


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


from functools import reduce


def get_data(name, version):
    soup = get_result(name, version)
    data0 = soup | get_index
    data1 = soup | get_table
    data2 = soup | get_ul

    data = data0 + data1 + data2

    merged = reduce(merge_two_dicts, data)
    return merged


def main():
    print(get_data('howdoi', '1.1.9'))


if __name__ == '__main__':
    main()


def parse_package_page(self, data_f):
    """
    Parse package page.
    """
    soup = bs4.BeautifulSoup(data_f.read())
    data = {}

    try:
        pass
    except Exception as error:
        print("There was an error during parsing: " + str(error))
        print("Ignoring this package.")
        data = {}
        data["files"] = []
        data["info"] = {}

    soup.decompose()
    return data
