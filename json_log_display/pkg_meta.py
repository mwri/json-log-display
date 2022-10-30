"""Package meta data."""

import sys

name = "json-log-display"
version = "0.0.1"
author = "Michael Wright"
author_email = "mjw@methodanalysis.com"
description = "Strict Text Template Parsing"
url = "https://github.com/mwri/json-log-display"

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

entry_points = {
    "console_scripts": [
        "jld=json_log_display.cli:jld",
    ],
}

python_requires = ">=3.6"
install_requires = ["ansicolors>=1.1.8"]

extras_require = {
    "dev": [
        "Sphinx==4.4.0",
        "sphinx-rtd-theme==1.0.0",
        "black==22.10.0",
        "isort==5.10.1",
    ],
}

package_data = {}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        attr_names = sys.argv[1:]
        attr_val = getattr(sys.modules[__name__], attr_names.pop(0))

        def display_val(val):
            if type(attr_val) == str:
                print(val)
            elif type(val) == list:
                for sub_val in val:
                    print(sub_val)
            elif type(val) == dict:
                print(repr(val))

        if type(attr_val) in (str, list):
            display_val(attr_val)
        elif type(attr_val) == dict:
            while len(attr_names) > 0 and type(attr_val) == dict:
                attr_val = attr_val[attr_names.pop(0)]
            display_val(attr_val)
