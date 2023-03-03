import argparse, argcomplete, requests, os, sys, arxiv, yaml
import tqdm
from commons import describe_paper, clean_text, log_arxiv, arxiv_url

def stream_bytes(pid, fn, chunk_size):
    if os.path.exists(fn): print("File exists!\nAbort."); sys.exit(1)
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
    
