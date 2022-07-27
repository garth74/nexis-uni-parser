# NexisUni Parser

This module can be used to convert Nexis Uni rich-text files to a tabular format.

## Usage

There are three main functions that this package provides.

### Convert an RTF file to plain text

Converting an RTF file to a plain text file can be achieved more directly by using pandoc. That said, I have included a function that will convert an RTF file to a plain text file. Under the hood it just uses [pandoc](https://pypi.org/project/pandoc/).

### Parse Nexis Uni Files

The result of parsing a nexisuni file is a gzipped JSON lines file. This can be read easily using pandas. I choose to convert to a compressed JSON lines file because the text data can get rather large. Writing it to Excel directly would add a dependency and would force all the data to be read into memory before writing the file. By streaming it directly into a JSON lines file, the memory consumption stays relatively low.

```python
from pathlib import Path
from nexisuni_parser import parse

inputfile = Path.home().joinpath("nexisuni-file.rtf")

output_filepath = parse(inputfile)

# Reading the data into a pandas dataframe is easy from here.

import pandas as pd

nexisuni_df = pd.read_json(str(output_filepath), compression="gzip", lines=True)

```
