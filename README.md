# Day-to-day utils

## `arxiv-utils`
- Download and log an arxiv from its `id`. 
    ```bash
    ./arxiv-utils.sh stream \
        --id {arxiv_id} \
        --out {output_file} \
        --chunksize {buffer_size_in_bytes(optional)} \
        --log {yaml_log_file(optional)}
    ```
- Search, stream and log a paper from its author and title:
    ```bash
    ./arxiv-utils.sh search \
        --title {author} \
        --author {author} \
        --log {yaml_log_file(optional)} \
        --stream (optional) \
        --chunksize {buffer_size_in_bytes(optional)}
    ```
- (recommended) add alias to `~/.bashrc`:
    ```
    alias arxiv-utils="path/to/arxiv-utils.sh
    ```
- **TODO**:
    - [ ] Yaml to actual database, [blog post](https://phoenixnap.com/kb/mysql-remote-connection)
    - [ ] Change pdf naming scheme: 
        ```
        import string
        parse_string = lambda x: "-".join([p.lower() for p in x.translate(str.maketrans("", "", string.punctuation)).split()])
        "_".join([
            parse_string(author),
            parse_string(title)
        ])+".pdf"
        ```
