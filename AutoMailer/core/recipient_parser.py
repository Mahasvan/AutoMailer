import csv
import re

def load_recipients(f_path: str) -> list[str]:
    recipients = []
    with open(f_path, newline = '', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for line in reader:
            if len(line) < 2:
                continue

            email = line[1]
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
            if not valid:
                continue

            recipients.append(line)
    print(recipients)
    return recipients


if __name__ == '__main__':
    load_recipients(r'data\input.csv')