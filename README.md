# Nexis Uni Parser

[![PyPI](https://img.shields.io/pypi/v/nexis-uni-parser.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/nexis-uni-parser.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/nexis-uni-parser)][python version]
[![License](https://img.shields.io/pypi/l/nexis-uni-parser)][license]

[![Read the documentation at https://nexis-uni-parser.readthedocs.io/](https://img.shields.io/readthedocs/nexis-uni-parser/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/garth74/nexis-uni-parser/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/garth74/nexis-uni-parser/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/nexis-uni-parser/
[status]: https://pypi.org/project/nexis-uni-parser/
[python version]: https://pypi.org/project/nexis-uni-parser
[read the docs]: https://nexis-uni-parser.readthedocs.io/
[tests]: https://github.com/garth74/nexis-uni-parser/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/garth74/nexis-uni-parser
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

This package can be used to convert NexisUni richtext files to jsonlines format.

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Nexis Uni Parser_ via [pip] from [PyPI]:

```console
pip install nexis-uni-parser
```

## Usage

There are two main functions that this package provides.

### Convert an RTF file to plain text

Converting an RTF file to a plain text file can be achieved directly by using pandoc. That said, I have included a function that will convert an RTF file to a plain text file since it could be useful. Under the hood, it just uses [pandoc](https://pypi.org/project/pandoc/).

```python
from pathlib import Path
from nexis_uni_parser import convert_rtf_to_plain_text

inputfile = Path.home().joinpath("nexisuni-file.rtf")
output_filepath = convert_rtf_to_plain_text(inputfile)

print(output_filepath)
>>> /Users/name/nexisuni-file.txt

```

### Parse Nexis Uni Files

The `parse` function can be used to parse a single file or a directory. Both produce a gzipped JSON lines file. I choose to convert to a compressed JSON lines file because the text data can get large if all files are read into memory.

```python
from pathlib import Path
from nexis_uni_parser import parse

inputfile = Path.home().joinpath("nexisuni-file.rtf")

output_filepath = parse(inputfile)

# Reading the data into a pandas dataframe is easy from here.

import pandas as pd

nexisuni_df = pd.read_json(str(output_filepath), compression="gzip", lines=True)

```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Nexis Uni Parser_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/garth74/nexis-uni-parser/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/garth74/nexis-uni-parser/blob/main/LICENSE
[contributor guide]: https://github.com/garth74/nexis-uni-parser/blob/main/CONTRIBUTING.md
[command-line reference]: https://nexis-uni-parser.readthedocs.io/en/latest/usage.html
