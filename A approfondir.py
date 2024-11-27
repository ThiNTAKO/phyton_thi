import re

def extract(log_file_path):
    # Define the regex pattern
    regex = r'(\d+\.\d+\.\d+\.\d+) - - \[([^\]]+)\] "(.*?)" (\d+) "(.*?)" "(.*?)"'
    data = {}  # Dictionary to store extracted data

    # Open the log file safely with a context manager
    with open(log_file_path, 'r') as log_file:
        for log_line in log_file:
            match = re.search(regex, log_line)

            if match:
                # Extract components of the log line
                ip_address = match.group(1)
                date_time = match.group(2)
                url = match.group(3)
                return_code = match.group(4)
                size = match.group(5)
                user_agent = match.group(6)

                # Remove any newline from the size value
                size = size.rstrip('\n')

                # Initialize default values for parameters
                param_numb = len(url.split('&')) if '&' in url else 0
                url_length = len(url)

                # Handle missing size with a default value
                if size == '-':
                    size = 0
                else:
                    try:
                        size = int(size)
                    except ValueError:
                        size = 0

                # Only process if the return code is a valid HTTP status
                try:
                    return_code = int(return_code)
                except ValueError:
                    continue

                if return_code > 0:
                    # Create a dictionary for the current log line
                    charc = {
                        "size": size,
                        "param_num": param_numb,
                        "length": url_length,
                        "return": return_code,
                    }

                    # Add the extracted information to the main data dictionary
                    if ip_address not in data:
                        data[ip_address] = []

                    data[ip_address].append(charc)

    return data

if __name__ == "__main__":
    log_file_path = "log_file.txt"
    extracted_data = extract(log_file_path)

    # Print the extracted data
    for ip, entries in extracted_data.items():
        print(f"IP Address: {ip}")
        for entry in entries:
            print(entry)

