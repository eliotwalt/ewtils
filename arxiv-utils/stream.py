import argparse, argcomplete, requests
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

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--id", help="arxiv id", required=True, type=arxiv_url)
    p.add_argument("--out", help="filename to write to", required=True)
    p.add_argument("--chunk_size", help="buffer size in bytes", required=False, default=2000)
    argcomplete.autocomplete(p)
    args = p.parse_args()
    stream_bytes(args.id, args.out, args.chunk_size)
    
