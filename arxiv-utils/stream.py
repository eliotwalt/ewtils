import argparse, argcomplete, requests, os, sys, arxiv, yaml
from pathlib import Path
import tqdm

def arxiv_url(id):
    return f"https://arxiv.org/pdf/{id}.pdf"

def stream_bytes(url, fn, chunk_size):
    print(f"Stremaing {url} to {fn}...")
    response = requests.get(url, stream=True)
    with open(fn, "wb") as f:
        for chunk in tqdm.tqdm(response.iter_content(chunk_size=chunk_size)):
            f.write(chunk)
    print("Done.")

def clean_text(txt):
    txt = " ".join([
        part.strip()
        for part in txt.split()
    ])
    return txt

def log_arxiv(pid, fn, log_f):
    paper = next(arxiv.Search(id_list=[pid]).results())
    data = {
        "id": pid,
        "title": paper.title,
        "first_author": paper.authors[0].name,
        "authors": [a.name for a in paper.authors],
        "date_published": paper.published,
        "date_updated": paper.updated,
        "abstract": clean_text(paper.summary),
        "fn": Path(fn).name
    }
    print(os.path.exists(log_f))
    if os.path.exists(log_f):
        with open(log_f) as f:
            logs = list(yaml.safe_load_all(f))
        print(len(logs))
    else: logs = list()
    print(len(logs))
    logs.append(data)
    print(len(logs))
    with open(log_f, "w") as f:
        yaml.dump(logs, f, sort_keys=False)

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--id", help="arxiv id", required=True)
    p.add_argument("--out", help="filename to write to", required=True)
    p.add_argument("--log", help="log file (optional)", required=False)
    p.add_argument("--chunk_size", help="buffer size in bytes (optional)", required=False, default=2000)
    argcomplete.autocomplete(p)
    args = p.parse_args()
    if os.path.exists(args.out): print("File exists!\nAbort."); sys.exit(1)
    args.url = arxiv_url(args.id)
    stream_bytes(args.url, args.out, args.chunk_size)
    if args.log: log_arxiv(args.id, args.out, args.log)
    
