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
        # Return as a tuple for easier CSV writing
        return (self.timestamp, self.hostname, self.process_type, self.log_type, self.action, self.application, self.tcp_socks_status)

if __name__ == "__main__":
    logs = []

    # Read the lines one by one
    with open("log_type.txt", "r") as fp:
        lines = fp.readlines()

    # Process each line
    for line in lines:
        line = line.strip()

        timestamp = line[0:15]
        hostname = line[16:26]
        process_type = line[27:46]
        log_type = line[49:64]
        action = line[66:82]
        application = line[83:94]
        tcp_socks_status = line[-11:]

        unLog = Log(timestamp, hostname, process_type, log_type, action, application, tcp_socks_status)
        logs.append(unLog)
    for log in logs:
        print(log.get_logs())

    with open("log_type_out.csv", mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(["Timestamp", "Hostname", "Process Type", "Log Type", "Action", "Application", "TCP Socks Status"])

        for log in logs:
            csvwriter.writerow(log.get_logs())  # Write each log entry
            print(log.get_logs())

