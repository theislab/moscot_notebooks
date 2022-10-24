#!/usr/bin/env python3
from typing import Any
from pathlib import Path
import argparse

_CNT = 0  # increment this when you want to rebuild the CI cache
_ROOT = Path.home() / ".cache" / "moscot"


def _print_message(func_name: str, path: Path, *, dry_run: bool = False) -> None:
    prefix = "[DRY RUN]" if dry_run else ""
    if path.is_file():
        print(f"{prefix}[Loading]     {func_name:>25} <- {str(path):>25}")
    else:
        print(f"{prefix}[Downloading] {func_name:>25} -> {str(path):>25}")


def _maybe_download_data(func_name: str, path: Path) -> Any:
    import moscot

    try:
        return getattr(moscot.datasets, func_name)(path=path)
    except Exception as e:
        print(f"File {str(path):>25} seems to be corrupted: {e}. Removing and retrying")
        path.unlink()

        return getattr(moscot.datasets, func_name)(path=path)


def main(args: argparse.Namespace) -> None:
    from moscot.datasets._datasets import __all__ as datasets

    all_datasets = datasets
    all_extensions = ["h5ad"] * len(datasets)

    if args.dry_run:
        for func_name, ext in zip(all_datasets, all_extensions):
            path = _ROOT / f"{func_name}.{ext}"
            _print_message(func_name, path, dry_run=True)
        return

    # could be parallelized, but on CI it largely does not matter (usually limited to 2 cores + bandwidth limit)
    for func_name, ext in zip(all_datasets, all_extensions):
        path = _ROOT / f"{func_name}.{ext}"

        _print_message(func_name, path)
        assert path.is_file(), path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download data used for tutorials/examples.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Do not download any data, just print what would be downloaded."
    )

    main(parser.parse_args())
