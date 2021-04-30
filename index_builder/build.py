import pathlib
from typing import Dict, List, Tuple


def build_index(path: str, packages: Dict[str, List[Tuple[str, str]]]) -> None:
    print("Generating index...")

    for package_name, files in packages.items():
        files_list = "".join(
            [f'<a href="{url}">{fname}</a><br>\n' for url, fname in sorted(files)]
        )
        parent = pathlib.Path(path) / package_name
        parent.mkdir(parents=True, exist_ok=True)
        print(package_name)
        print(files_list)
        (parent / "index.html").write_text(
            f"<!DOCTYPE html><html><body>\n{files_list}</body></html>"
        )
    package_list = "".join(
        [f'<a href="{p}/">{p}</a><br>\n' for p in sorted(packages.keys())]
    )
    index_dir = pathlib.Path(path)
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / "index.html").write_text(
        f"<!DOCTYPE html><html><body>\n{package_list}</body></html>"
    )
