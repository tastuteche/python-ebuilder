gentoo_pkg = {
    "beautifulsoup4": "dev-python/beautifulsoup",
    "pocketsphinx": "app-accessibility/pocketsphinx",
    "SpeechRecognition": "app-accessibility/speechrecognition",
    "EbookLib": "dev-python/ebooklib",
    "scipy": "sci-libs/scipy",
    "scikit-learn": "sci-libs/scikits_learn",

}


def query_gentoo_pkg(name):
    if name in gentoo_pkg:
        return gentoo_pkg[name]
    return 'dev-python/' + name
