import datetime
import sys

try:
    # Optional: allow user to specify a format or timezone via command line
    import argparse
    parser = argparse.ArgumentParser(description='Get current date and time.')
    parser.add_argument('--format', type=str, default='%Y-%m-%d %H:%M:%S',
                        help='Datetime format string (default: %%Y-%%m-%%d %%H:%%M:%%S)')
    parser.add_argument('--utc', action='store_true', help='Show time in UTC instead of local time')
    args = parser.parse_args()

    def get_current_datetime(fmt: str = '%Y-%m-%d %H:%M:%S', use_utc: bool = False) -> str:
        now = datetime.datetime.utcnow() if use_utc else datetime.datetime.now()
        return now.strftime(fmt)

    dt = get_current_datetime(fmt=args.format, use_utc=args.utc)
    print(f"Current date and time: {dt}")
except Exception as e:
    print(f"Error retrieving date and time: {e}", file=sys.stderr)
    sys.exit(1) 