from pathlib import Path

def load_data(path):
    path = Path(path)
    if path.suffix == ".csv":
        usernames, domains, extensions = load_csvData(path)
    elif path.suffix == ".txt":
        usernames, domains, extensions = load_txtData(path)
    elif path.suffix == ".json":
        usernames, domains, extensions = load_jsonData(path)
    else:
        print(f"[ERROR] Unsupported file extension: {path.suffix}")
        return (None, None, None)

    if usernames is None or domains is None or extensions is None:
        return (None, None, None)

    usernames.reverse()
    domains.reverse()
    extensions.reverse()

    return (usernames, domains, extensions)

def load_csvData(path):
    try:
        import csv
    except:
        print("[ERROR]: error importing csv module")
        return (None, None, None)
    usernames = []
    domains = []
    extensions = []

    with open(path) as file:
        data = csv.reader(file)
        i = 0
        for line in data:
            if i == 0:
                i +=1
                continue
            usernames.append(line[0])
            domains.append(line[1])
            extensions.append(line[2])

    return (usernames, domains, extensions)

def load_txtData(path):
    usernames = []
    domains = []
    extensions = []

    with open(path) as file:
        data = file.readlines()

    for email in data:
        email = email.strip()
        try:
            username, domain_extension = email.split("@")
            domain, extension = domain_extension.rsplit(".", 1)
        except:
            continue

        usernames.append(username)
        domains.append(domain)
        extensions.append(extension)
    
    return (usernames, domains, extensions)


def load_jsonData(path):
    try:
        import json
    except:
        print("[ERROR]: error importing json module")
        return (None, None, None)

    usernames = []
    domains = []
    extensions = []

    try:
        with open(path, "r") as file:
            data = json.load(file)

        for entry in data:
            if "username" in entry and "domain" in entry and "extension" in entry:
                usernames.append(entry["username"])
                domains.append(entry["domain"])
                extensions.append(entry["extension"])
            else:
                continue

    except:
        print("[ERROR]: error loading data from json")
        return (None, None, None)

    return (usernames, domains, extensions)