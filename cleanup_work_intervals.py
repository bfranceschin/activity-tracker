import argparse
import datetime as dt
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove work intervals longer than 8 hours and write a cleaned copy."
    )
    parser.add_argument(
        "--input",
        default="work_intervals.json",
        type=Path,
        help="Path to the source work intervals JSON file (default: work_intervals.json).",
    )
    parser.add_argument(
        "--output",
        default="work_intervals.cleaned.json",
        type=Path,
        help="Path for the cleaned JSON output (default: work_intervals.cleaned.json).",
    )
    parser.add_argument(
        "--threshold-hours",
        default=8,
        type=float,
        help="Duration threshold in hours for pruning intervals (default: 8).",
    )
    return parser.parse_args()


def load_intervals(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def serialize_intervals(intervals: list[dict[str, dt.datetime]]) -> list[dict[str, str]]:
    return [{"start": i["start"].isoformat(), "end": i["end"].isoformat()} for i in intervals]


def filter_intervals(
    intervals: list[dict[str, str]], threshold: dt.timedelta
) -> tuple[list[dict[str, dt.datetime]], list[dict[str, dt.datetime]]]:
    kept: list[dict[str, dt.datetime]] = []
    removed: list[dict[str, dt.datetime]] = []

    for interval in intervals:
        start = dt.datetime.fromisoformat(interval["start"])
        end = dt.datetime.fromisoformat(interval["end"])
        duration = end - start

        target_list = kept if duration <= threshold else removed
        target_list.append({"start": start, "end": end})

    return kept, removed


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    raw_intervals = load_intervals(args.input)
    threshold = dt.timedelta(hours=args.threshold_hours)

    kept, removed = filter_intervals(raw_intervals, threshold)

    args.output.write_text(
        json.dumps(serialize_intervals(kept), indent=2),
        encoding="utf-8",
    )

    print(
        f"Pruned {len(removed)} interval(s) longer than {threshold}. "
        f"Cleaned data written to {args.output}."
    )

    if removed:
        print("Removed intervals:")
        for interval in removed:
            duration = interval["end"] - interval["start"]
            print(
                f"  {interval['start'].isoformat()} -> {interval['end'].isoformat()} "
                f"({duration})"
            )


if __name__ == "__main__":
    main()

