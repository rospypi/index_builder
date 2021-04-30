import pathlib
from typing import Dict, List, Sequence, Tuple

import git


def load_local_packages(paths: Sequence[str]) -> Dict[str, List[Tuple[str, str]]]:
    print("Loading local packages...")

    packages: Dict[str, List[Tuple[str, str]]] = {}
    for local_path in paths:
        for dirname in pathlib.Path(local_path).glob("*"):
            for fname in dirname.glob("*"):
                package_name = fname.parent.name
                packages.setdefault(package_name, [])
                packages[package_name].append(
                    (
                        f"/{fname}",
                        fname.name,
                    )
                )

    return packages


def load_repository_packages(
    remote: git.Remote, prefix: str, host: str = "github.com"
) -> Dict[str, List[Tuple[str, str]]]:
    print("Loading repository packages...")

    remote.fetch()
    url = pathlib.Path(remote.url)
    raw_url = pathlib.Path(host) / url.parent.name / url.stem / "raw"

    branches: List[str] = ["any"]
    for platform in ("Linux", "Darwin", "Windows"):
        for version in ("3.6", "3.7", "3.8"):
            branches.append(platform + "_" + version)
    if prefix:
        for idx in range(len(branches)):
            branches[idx] += "_" + prefix

    packages: Dict[str, List[Tuple[str, str]]] = {}
    for branch in branches:
        if branch in remote.refs:
            for t in remote.refs[branch].commit.tree.trees:
                for b in t.blobs:
                    packages.setdefault(t.name, [])
                    packages[t.name].append(
                        (
                            f"https://{raw_url}/{branch}/{t.name}/{b.name}",
                            b.name,
                        )
                    )

    return packages
