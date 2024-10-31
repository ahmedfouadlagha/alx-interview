#!/usr/bin/python3
"""
Log parsing
"""

import sys

if __name__ == '__main__':

    # Initialize variables for total file size and line count
    filesize, count = 0, 0

    # Define valid status codes and initialize a dictionary for counting occurrences
    codes = ["200", "301", "400", "401", "403", "404", "405", "500"]
    stats = {k: 0 for k in codes}

    # Function to print current statistics
    def print_stats(stats: dict, filesize: int) -> None:
        print("File size: {:d}".format(filesize))
        for k, v in sorted(stats.items()):
            if v:
                print("{}: {}".format(k, v))

    try:
        # Process each line from stdin
        for line in sys.stdin:
            count += 1
            data = line.split()

            # Extract and count status code if it exists in the line
            try:
                status_code = data[-2]
                if status_code in stats:
                    stats[status_code] += 1
            except IndexError:
                pass  # Skip if line doesn't have a valid status code position

            # Add file size from the line if it's valid
            try:
                filesize += int(data[-1])
            except (ValueError, IndexError):
                pass  # Skip if file size is missing or not an integer

            # Print stats every 10 lines
            if count % 10 == 0:
                print_stats(stats, filesize)

        # Print final statistics after processing all lines
        print_stats(stats, filesize)

    except KeyboardInterrupt:
        # Print stats on keyboard interruption and re-raise the exception to exit
        print_stats(stats, filesize)
        raise
