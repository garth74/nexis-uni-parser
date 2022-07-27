import gzip
import json
import logging
import re
import typing as t
from hashlib import md5
from itertools import repeat
from pathlib import Path

import pandoc
from unidecode import unidecode

Match = re.Match[str]
AnyMatch = Match | t.Any
AnyMatchGenerator = t.Generator[tuple[AnyMatch, AnyMatch, AnyMatch], None, None]
ErrorOptions = t.Union[t.Literal["ignore"], t.Literal["strict"]]


class AlreadyParsedError(Exception):
    """This text has already been parsed or a file with the exact same content has been parsed."""


def _getid(text: str):
    """Creates a unique id using the md5 algorithm."""
    return md5(text.encode("utf-8")).hexdigest()


def _neighborhood(iterable: t.Iterable[Match], next_default: t.Any = None) -> AnyMatchGenerator:
    """Loop through an iterable yielding its previous and following item."""
    iterator = iter(iterable)
    prev_item = None
    current_item = next(iterator, next_default)
    for next_item in iterator:
        yield (prev_item, current_item, next_item)
        prev_item = current_item
        current_item = next_item
    yield (prev_item, current_item, None)


class Parser:
    """This class just stores the tokens and regular expressions used in parsing the nexisuni files."""

    logger = logging.getLogger(__name__)

    _sections = [
        ("{prefix}_Length", r"(Length):"),
        ("{prefix}_Section", r"(Section):?"),
        ("{prefix}_Byline", r"(Byline):?"),
        ("{prefix}_Load_Date", r"(Load-Date):?"),
        ("{prefix}_Client_Matter", r"(Client/Matter):?"),
        ("{prefix}_Search_Type", r"(Search Type):?"),
        ("{prefix}_Narrowed_by", r"(Narrowed by):?"),
        ("{prefix}_Date_and_Time", r"(Date and Time):?"),
        ("{prefix}_Job_Number", r"(Job Number):?"),
        ("{prefix}_Body", r"(Body)"),
    ]
    patterns: dict[str, re.Pattern[str]] = {}

    def __init__(self):
        self._pattern = None
        self._parsed: set[str] = set()

    def get_pattern(self, prefix: str):
        """Get a compiled regular expression given a prefix."""
        if prefix not in self.patterns:
            sections = [(desc.format(prefix=prefix), pattern) for desc, pattern in self._sections]
            pattern = "|".join(r"(?P<%s>%s)" % pair for pair in sections)
            self.patterns[prefix] = re.compile(pattern, flags=re.IGNORECASE)
        return self.patterns[prefix]

    def parse_key_value_pairs(self, prefix: str, raw_text: str):
        """Parse key value pairs from the nexis uni raw text.

        Creates a dictioanry of key value pairs from instances of r"(.*):(.*)"
        """
        sections: dict[t.Any, t.Any] = {f"{prefix}_raw_text": raw_text}
        pattern = self.get_pattern(prefix)
        matches = pattern.finditer(raw_text)
        for _, mo, next_mo in _neighborhood(matches):
            if mo is None:
                continue

            kind = mo.lastgroup
            start = mo.end()  # does not include kind in value
            if next_mo is None:  # last match object
                end = len(raw_text)
            else:  # start of next match object
                end = next_mo.start()

            value = raw_text[start:end]
            sections[kind] = value

        return sections

    def _check_parsed(self, raw_text: str, errors: ErrorOptions):
        id_ = _getid(raw_text)
        if id_ in self._parsed:
            if errors == "strict":
                raise AlreadyParsedError("To remove this error, make sure the `errors` parameter is set to 'ignore'.")
        self._parsed.add(id_)

    def parse(self, raw_text: str, errors: ErrorOptions):
        """Parses the contents of a downloaded Nexis Uni file."""
        # Make sure the data is unicode
        text = unidecode(raw_text).strip()

        # Check that it hasn't already been done
        self._check_parsed(text, errors)

        # Extract the job metadata, tocs, and articles
        chunk, *articles = text.split("End of Document")  # 99 articles rn
        long_ass_line = "----------------------------------------"
        first_article = chunk[chunk.rfind(long_ass_line) + len(long_ass_line) :]
        articles.insert(0, first_article)
        chunk = chunk.replace(first_article, "")
        job_metadata, *tocs = re.split(r"\n\d{1,3}\.\n", chunk)

        # Extract the metadata, tocs, and articles from the items
        job_metadata = self.parse_key_value_pairs("job_metadata", job_metadata)

        # Parse the key value pairs
        tocs_ = map(self.parse_key_value_pairs, repeat("toc"), tocs)
        articles_ = map(self.parse_key_value_pairs, repeat("article"), articles)
        return [{**job_metadata, **toc_data, **article_data} for toc_data, article_data in zip(tocs_, articles_)]

    def _parse_file(self, file: Path | str, errors: ErrorOptions):
        doc = pandoc.read(file=Path(file).as_posix())  # type: ignore
        plain_text = pandoc.write(doc, options=["--to", "plain"])  # type: ignore
        return self.parse(plain_text, errors)

    def parse_file(self, file: Path | str, errors: ErrorOptions = "strict"):
        """Parse a nexis uni file."""
        assert errors in {"strict", "ignore"}, "`errors` parameter must be either 'strict' or 'ignore'"
        self.logger.info(f"Parsing {Path(file).name}")
        try:
            yield from self._parse_file(file, errors)
        except AlreadyParsedError as e:
            if errors == "strict":
                raise e
            yield None

    def parse_directory(self, directory: str | Path, errors: ErrorOptions = "ignore", recursive: bool = False):
        """Parse all the .rtf nexis uni files in a directory."""
        self.logger.info(f"Parsing contents of {directory}")
        path = Path(directory)
        method = Path.rglob if recursive else Path.glob
        for file in method(path, "*.[rR][tT][fF]"):
            yield from self.parse_file(file, errors=errors)


def convert_rtf_to_plain_text(rtf_file: Path | str):
    """Create a plain text file from an RTF file.

    Uses the same name as the original file, changing only the extension.
    """
    rtf_file = Path(rtf_file)
    doc = pandoc.read(file=rtf_file.as_posix())  # type: ignore
    plain_text = pandoc.write(doc, options=["--to", "plain"])  # type: ignore
    new_file = rtf_file.with_suffix(".txt")
    new_file.write_text(plain_text, errors="ignore")
    return new_file


def parse(
    inputpath: Path | str,
    output_filepath: t.Optional[Path | str] = None,
    recursive: bool = False,
    errors: ErrorOptions = "ignore",
):
    """Parse a file or directory. The result is a compressed json lines file."""
    inpath = Path(inputpath)
    outpath = Path(output_filepath or inpath.with_suffix("jsonl.gz"))
    parser = Parser()
    with gzip.open(outpath, mode="wt") as gz:
        if inpath.is_dir():
            data = parser.parse_directory(inpath, errors, recursive)
        else:
            data = parser.parse_file(inpath, errors)
        gz.writelines(map(json.dumps, filter(None, data)))
    return outpath
