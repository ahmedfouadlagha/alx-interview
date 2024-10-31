#!/usr/bin/python3
"""
Log parsing
"""

import sys
import signal

# Initialize counters and dictionary for file size and status codes
total_size = 0
status_counts = {str(code): 0 for code in [200, 301, 400, 401, 403, 404, 405, 500]}
line_count = 0

# Function to print the metrics
def print_stats():
    print("File size: {}".format(total_size))
    for code in sorted(status_counts.keys()):
        if status_counts[code] > 0:
            print("{}: {}".format(code, status_counts[code]))

# Handle keyboard interrupt (CTRL + C)
def signal_handler(sig, frame):
    print_stats()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Read from stdin line by line
try:
    for line in sys.stdin:
        line = line.strip()
        parts = line.split()

        # Validate format and parse elements
        if len(parts) >= 7 and parts[2] == "-" and parts[5].startswith('"GET') and parts[6].startswith('/projects/260'):
            try:
                # Extract file size and status code
                status_code = parts[-2]
                file_size = int(parts[-1])

                # Update total file size
                total_size += file_size

                # Update status code count if valid
                if status_code in status_counts:
                    status_counts[status_code] += 1

                line_count += 1

                # Print stats every 10 lines
                if line_count % 10 == 0:
                    print_stats()

            except (ValueError, IndexError):
                # Skip line if there’s an error in file size or status code format
                continue
except KeyboardInterrupt:
    pass
finally:
    # Print stats one last time at the end or on interruption
    print_stats()
