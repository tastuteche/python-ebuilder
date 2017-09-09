import urllib.request
from bs4 import BeautifulSoup
from pymonad.Maybe import Nothing, Just


def get_result(name_version):
    theurl = "http://gpo.zugaina.org/Search?search=%s" % name_version
    thepage = urllib.request.urlopen(theurl)

    soup = BeautifulSoup(thepage, "lxml")

    # <div id="search_results">
    search_results = soup.find('div', id="search_results")
    if search_results:
        return Just(search_results)
    else:
        return Nothing


def get_url(search_results):
    rtn = []
    for a in search_results.find_all('a'):
        rtn.append(a['href'])
    if len(rtn) == 0:
        return Nothing
    else:
        return Just(rtn)


def get_category(url_list):
    if len(url_list) == 1:
        return Just(url_list[0])
    else:
        return Nothing


def get_dir(name_version):
    folder = get_result(name_version) >> get_url >> get_category
    if folder == Nothing:
        return ""
    else:
        return folder.value


def main():
    print(get_dir('rtv-1.13.0'))
    print(get_dir('howdoi-1.1.9'))


if __name__ == '__main__':
    main()
