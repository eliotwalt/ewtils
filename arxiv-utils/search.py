import argparse, argcomplete, requests, os, sys, arxiv, yaml

from commons import describe_paper, log_arxiv, log_not_arxiv
from stream import stream_bytes

def search_paper_by_author_and_title(author, title):
    """
    data keys are `au` for author and `ti` for title. Values are strings
    additional_data is used to filter the results. the keys are attributes of arxiv.Result, e.g. `date_published`
    """
    assert author or title
    data = {"ti": title, "au": author}
    query_string = " AND ".join([f"{key}:{value}" for key, value in data.items() if value is not None])
    try: paper = next(arxiv.Search(query=query_string, max_results=1).results())
    except StopIteration: return None
    return paper.entry_id.split("/")[-1]
    
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--title", help="Paper title")
    p.add_argument("--author", help="Paper author")
    p.add_argument("--stream", help="whether to stream the pdf or not", action="store_true")
    p.add_argument("--chunk_size", help="streaming buffer size in bytes (optional)", required=False, default=2000)
    p.add_argument("--out", help="output file if stream")
    p.add_argument("--log", help="log file (optional)")
    args = p.parse_args()
    if args.stream: assert args.out is not None
    pid = search_paper_by_author_and_title(args.author, args.title)
    if pid:
        print(f"Found arXiv:{pid}")
        if args.stream:
            stream_bytes(pid, args.out, args.chunk_size)
        if args.log:
            log_arxiv(pid, args.log)
    else:
        print(f'No results found for {args.author}, {args.title}')
        if args.log:
            log_not_arxiv(args.author, args.title, args.log)
        