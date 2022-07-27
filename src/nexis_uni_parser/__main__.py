"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Nexis Uni Parser."""


if __name__ == "__main__":
    main(prog_name="nexis-uni-parser")  # pragma: no cover
