import argparse
import pandas as pd
import re

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help='Path to the raw file')
    parser.add_argument('output_file', help='Path where the CSV results will be stored')
    parser.add_argument('--status', type=int, default=200, help='Filter by log status input')
    parser.add_argument('--verbose', action='store_true', help='print progress of the script')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    status = args.status
    verbose = args.verbose

    line_num = 0
    skipped_lines = 0
    results = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                line_num += 1
                parsed = parse_line(line)
                if parsed is None:
                    if verbose:
                        skipped_lines += 1
                        print(f"Warning: skipping malformed line {line_num}")
                    continue
                if parsed['status'] != status:
                    continue
                results.append(parsed)
    except FileNotFoundError:
        print(f'Error: File was not found!')
        raise SystemExit(1) #Used to exit the code without traceback errors
    
    df = pd.DataFrame(results, columns=['timestamp', 'method', 'endpoint', 'status', 'ip', 'user_agent'])
    df.to_csv(output_file, index=False)

    if verbose: #To print the verbose flag
        print(f"Wrote {len(df)} rows to {output_file}")
        print(f'Total lines skipped: {skipped_lines}') #Total lines skipped
    
def parse_line(line: str):
    # Required fields + optional user agent (rest of line)
    pattern = (
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+'
        r'(?P<method>GET|POST|PUT|DELETE)\s+'
        r'(?P<endpoint>/\S+)\s+'
        r'(?P<status>\d{3})\s+'
        r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'
        r'(?:\s+(?P<user_agent>.*))?$'
    )

    m = re.match(pattern, line)
    if not m:
        return None

    data = m.groupdict()

    # Cast status to int
    data["status"] = int(data["status"])

    # Normalize optional user agent
    if data["user_agent"] is not None:
        data["user_agent"] = data["user_agent"].strip() or None

    return data



if __name__ == '__main__':
    main()