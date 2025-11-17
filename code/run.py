import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path

from open_ephys.analysis import Session
import numpy as np


def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def save_event_times(
    save_as: Path,
    event_times: np.ndarray,
    fmt: str = '%.6f',
    newline: str = '\n'
):
    """Save event times as one float in seconds per line -- same as CatGT and expected by our other steps."""
    np.savetxt(save_as, event_times.squeeze(), fmt=fmt, newline=newline)


def capsule_main(
    data_path: Path,
    results_path: Path,
    oebin_pattern: str,
):
    logging.info("Exporting Open Ephys TTL events to text.\n")

    oebin_paths = list(data_path.glob(oebin_pattern))
    if not oebin_paths:
        raise ValueError(f"No structure.oebin found within {data_path}, using pattern {oebin_pattern}.")

    oebin_path = oebin_paths[0]
    logging.info(f"Found structure.oebin: {oebin_path}")

    session_dir = oebin_path.parent.parent.parent.parent
    logging.info(f"Using Open Ephys session dir: {session_dir}")

    session = Session(session_dir)
    logging.info(f"Loaded Open Ephys session: {session}")

    for record_node_index, record_node in enumerate(session.session.recordnodes):
        logging.info(f"Extracting events from record node: {record_node}")
        for recording_index, recording in enumerate(session.recordings):
            logging.info(f"Extracting events from recording: {recording}")

            logging.info(f"Loading TTL events dataframe.")
            events_dataframe = recording.events

            event_timestamps = events_dataframe['timestamp']
            event_on_selector = events_dataframe['state'] == 1
            event_streams = events_dataframe['stream_name']
            event_lines = events_dataframe['line']
            for event_stream in np.unique(event_streams):
                logging.info(f"Extracting from event stream {event_stream}.")
                event_stream_selector = event_streams == event_stream

                for event_line in np.unique(event_lines):
                    logging.info(f"Extracting ON events from line {event_line}.")
                    event_line_selector = event_lines == event_line
                    timestamps = event_timestamps[event_on_selector & event_stream_selector & event_line_selector]

                    line_output_path = Path(results_path, f"{session_dir.stem}-node-{record_node_index}-rec-{recording_index}-{event_stream}-line-{event_line}.txt")
                    logging.info(f"Writing events to {line_output_path}")
                    line_output_path.parent.mkdir(exist_ok=True, parents=True)
                    save_event_times(line_output_path, timestamps)


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
