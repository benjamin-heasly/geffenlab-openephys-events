import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path


def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def capsule_main(
    data_path: Path,
    results_path: Path,
    oebin_pattern: str,
):
    logging.info("Exporting Open Ephys TTL events to .txt.\n")

    logging.warning("WIP...")

    logging.info("OK\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Export ecephys sorting resluts to Phy.")

    parser.add_argument(
        "--data-root", "-d",
        type=str,
        help="Where to find and read input data files. (default: %(default)s)",
        default="/data"
    )
    parser.add_argument(
        "--results-root", "-r",
        type=str,
        help="Where to write output result files. (default: %(default)s)",
        default="/results"
    )
    parser.add_argument(
        "--oebin-pattern", "-o",
        type=str,
        help="Pattern to match structure.oebin within an Open Ephys recording dicrectory. (default: %(default)s)",
        default="**/structure.oebin"
    )

    cli_args = parser.parse_args(argv)
    data_path = Path(cli_args.data_root)
    results_path = Path(cli_args.results_root)
    try:
        capsule_main(
            data_path=data_path,
            results_path=results_path,
            oebin_pattern=cli_args.oebin_pattern,
        )
    except:
        logging.error("Error exporting to Open Ephys events.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
