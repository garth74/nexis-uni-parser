# NexisUni Parser

This module can be used to convert Nexis Uni rich-text files to a tabular format.

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
