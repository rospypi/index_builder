import contextlib
import pathlib
import tempfile
from typing import ContextManager, Iterator, List, Optional

import click
import git

from .build import build_index
from .packages import load_local_packages, load_repository_packages


@contextlib.contextmanager
def _load_remote_git_repository(url: str) -> Iterator[git.Repo]:
    print(f"Cloning {url} ...")
    with tempfile.TemporaryDirectory() as td:
        yield git.Repo.clone_from(url, td)


@contextlib.contextmanager
def _load_local_git_repository(path: pathlib.Path) -> Iterator[git.Repo]:
    yield git.Repo(path, search_parent_directories=True)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@cli.command(help="build index html from local files")
@click.argument("out", type=str)
@click.argument("local_dirs", nargs=-1)
def local(out: str, local_dirs: List[str]) -> None:
    packages = load_local_packages(local_dirs)
    build_index(out, packages)


@cli.command(help="build index html from git repository")
@click.argument("out", type=str)
@click.option("--url", default=None, type=str)
@click.option(
    "--path", default=None, type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option("--prefix", default="", type=str)
def repo(out: str, url: Optional[str], path: Optional[click.Path], prefix: str) -> None:
    if path is None and url is None:
        raise click.BadArgumentUsage("either --url or --path is required")

    if path is not None and url is not None:
        raise click.BadArgumentUsage(
            "cannot use both --url and --path at the same time"
        )

    context: ContextManager[git.Repo]
    if url is not None:
        context = _load_remote_git_repository(url)
    else:
        assert path is not None

        context = _load_local_git_repository(pathlib.Path(str(path)))

    with context as repo:
        origin = repo.remotes.origin
        origin.fetch()
        packages = load_repository_packages(origin, prefix)

    build_index(out, packages)


if __name__ == "__main__":
    cli()
