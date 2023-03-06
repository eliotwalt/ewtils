import argparse, argcomplete, requests, os, sys, arxiv, yaml
import tqdm
from commons import describe_paper, clean_text, log_arxiv, arxiv_url
import string
from copy import copy
from pathlib import Path
alphabet = list(string.ascii_lowercase)

def stream_bytes(pid, fn, chunk_size):
    if os.path.exists(fn): 
        print("File exists! Renaming...")
        i = 0
        fn_ = copy(fn)
        while os.path.exists(fn_):
            fn_ = Path(fn).stem+alphabet[i]+".pdf"
            i += 1
        fn = str(fn_)
        print(f"New filename: {fn_}")
    url = arxiv_url(pid)
    print(f"Stremaing {url} to {fn}...")
    response = requests.get(url, stream=True)
    with open(fn, "wb") as f:
        for chunk in tqdm.tqdm(response.iter_content(chunk_size=chunk_size)):
            f.write(chunk)
    print("Done.")

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--id", help="arxiv id", required=True)
    p.add_argument("--out", help="filename to write to", required=True)
    p.add_argument("--log", help="log file (optional)", required=False)
    p.add_argument("--chunk_size", help="buffer size in bytes (optional)", required=False, default=2000)
    argcomplete.autocomplete(p)
    args = p.parse_args()    
    stream_bytes(args.id, args.out, args.chunk_size)
    if args.log: log_arxiv(args.id, args.log)
    
