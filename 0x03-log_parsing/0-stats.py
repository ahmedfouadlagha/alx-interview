#!/usr/bin/python3
"""
Reads stdin line by line and computes metrics.

Input format: <IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>
After every 10 lines and/or a keyboard interruption (CTRL + C), prints statistics from the beginning:
- Total file size: File size: <total size>
- Number of lines by status code:
  - Status code: <number>
Status codes: 200, 301, 400, 401, 403, 404, 405, 500
"""

import sys
from collections import defaultdict

def print_statistics(total_size, status_codes):
    """Prints statistics."""
    print("Total file size: {}".format(total_size))
    for code in sorted(status_codes.keys()):
        print("{}: {}".format(code, status_codes[code]))

def parse_line(line):
    """Parses a line and extracts IP address, status code, and file size."""
    try:
        parts = line.split()
        ip_address = parts[0]
        status_code = int(parts[-2])
        file_size = int(parts[-1])
        return ip_address, status_code, file_size
    except Exception:
        return None, None, None

def main():
    """Main function."""
    total_size = 0
    status_codes = defaultdict(int)
    line_count = 0

    try:
        for line in sys.stdin:
            ip_address, status_code, file_size = parse_line(line.strip())
            if ip_address is None:
                continue

            total_size += file_size
            status_codes[status_code] += 1
            line_count += 1

            if line_count % 10 == 0:
                print_statistics(total_size, status_codes)

    except KeyboardInterrupt:
        print_statistics(total_size, status_codes)
        sys.exit(0)

if __name__ == "__main__":
    main()