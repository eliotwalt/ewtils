import argparse, yaml, sys, json
from commons import write_logs, read_logs

def rm(args):
    logs = read_logs(args.log)
    condition = lambda x: args.title.lower()==x["title"].lower() and args.author.lower() in [part.lower() for part in x["first_author"]]
    for i, log in enumerate(logs):
        if condition(log):
           item = logs.pop(i)
           print(f"Deleted item {i}:")
           print(json.dumps(item))
           item.pop("abstract")
           break
    write_logs(logs, args.log)    

def search(args):
    logs = read_logs(args.log)
    if args.author and args.title: condition = lambda x: args.title.lower()==x["title"].lower() and args.author.lower() in [part.lower() for part in x["first_author"]]
    elif args.author: condition = lambda x: args.author.lower() in [part.lower() for part in x["first_author"]]
    else: condition = lambda x: args.title.lower()==x["title"].lower()
    cnt = 0
    for i, log in enumerate(logs):
        if condition(log):
           item = logs.pop(i)
           item.pop("abstract")
           print(f"Found item {i}:")
           print(json.dumps(item))
           cnt += 1
    print(f"Found {cnt} papers")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", help="title")
    p.add_argument("--author", help="author")
    p.add_argument("--log", help="log file", required=True)
    args = p.parse_args(sys.argv[2:])
    action = sys.argv[1]
    assert action in ["rm", "search"]
    assert args.author or args.title
    action_map = {"rm": rm, "search": search}
    action_map[action](args)

if __name__=="__main__": main()