import arxiv, yaml, os

def read_logs(path):
    try:
        with open(path) as f:
            logs = list(yaml.safe_load(f))
        return logs
    except: 
        print("could not load log file")
        sys.exit(1)

def write_logs(logs, path):
    with open(path, "w") as f:
        yaml.dump(logs, f, sort_keys=False)

def arxiv_url(id):
    return f"https://arxiv.org/pdf/{id}.pdf"

def clean_text(txt):
    txt = " ".join([
        part.strip()
        for part in txt.split()
    ])
    return txt

def log_arxiv(pid, log_f):
    print(f"logging {pid} in {log_f}")
    data = describe_paper(pid)
    if os.path.exists(log_f):
        logs = read_logs(log_f)
        for log in logs:
            if "id" in log.keys() and log["id"] == pid: 
                print("{} already in logs.".format(pid))
                return None
    else: logs = list()
    logs.append(data)
    write_logs(log_f, logs)
    return None

def log_not_arxiv(author, title, log_f):
    print(f"logging (not arxiv) {author}, '{title}' in {log_f}")
    if os.path.exists(log_f):
        with open(log_f) as f:
            logs = list(yaml.safe_load(f))
        for log in logs:
            if log["first_author"] == author and log["title"] == title: 
                print(f"{author}, '{title}' already in logs.")
                return None
    else: logs = list()
    logs.append({"first_author": author, "title": title})
    with open(log_f, "w") as f:
        yaml.dump(logs, f, sort_keys=False)
    return None

def describe_paper(pid):
    paper = next(arxiv.Search(id_list=[pid]).results())
    data = {
        "id": pid,
        "title": paper.title,
        "first_author": paper.authors[0].name,
        "authors": [a.name for a in paper.authors],
        "date_published": paper.published,
        "date_updated": paper.updated,
        "abstract": clean_text(paper.summary),
    }
    return data