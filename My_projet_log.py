import csv

class Log:
    def __init__(self, timestamp, hostname, process_type, log_type, action, application, tcp_socks_status):
        self.timestamp = timestamp
        self.hostname = hostname
        self.process_type = process_type
        self.log_type = log_type
        self.action = action
        self.application = application
        self.tcp_socks_status = tcp_socks_status

    def get_logs(self):
        return (self.timestamp, self.hostname, self.process_type, self.log_type, self.action, self.application, self.tcp_socks_status)

def main():
    logs = []

    input_file = r"c:\Users\thier\Desktop\phyton_thi\log_typ.txt"
    output_file = r"c:\Users\thier\Desktop\phyton_thi\log_type_out.csv"

    try:
        # Read lines from the input file
        with open(input_file, "r") as fp:
            lines = fp.readlines()

        # Process each line
        for line in lines:
            line = line.strip()
            if len(line) < 95:  # Minimum length check for expected format
                print(f"Skipped invalid line: {line}")
                continue

            try:
                timestamp = line[0:15]
                hostname = line[16:26].strip()
                process_type = line[27:46].strip()
                log_type = line[49:64].strip()
                action = line[66:82].strip()
                application = line[83:94].strip()
                tcp_socks_status = line[-11:].strip()

                log_entry = Log(timestamp, hostname, process_type, log_type, action, application, tcp_socks_status)
                logs.append(log_entry)

            except IndexError:
                print(f"Error processing line: {line}")
                continue

        # Write to CSV
        with open(output_file, mode='w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Timestamp", "Hostname", "Process Type", "Log Type", "Action", "Application", "TCP Socks Status"])
            for log in logs:
                csvwriter.writerow(log.get_logs())
                print(log.get_logs())

        print(f"Logs successfully written to {output_file}")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

