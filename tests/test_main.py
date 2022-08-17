from pathlib import Path

from nexis_uni_parser import parse


def test_parser(tmp_path: Path) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    outpath = d / "name"
    parse(Path(__file__).parent.joinpath("Files(100).RTF"), outpath)
