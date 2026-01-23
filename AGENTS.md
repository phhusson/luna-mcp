Code is in server.py

server.py's `__main__` is used for making tests so that `uv run server.py` runs and displays some state and tests

A sample JSON can be found in `lunatracker_logbook.json`

The server is an `uv` script, you can run it with `uv run server.py`, import parts of it with `uv run python -c 'from server import add_poo'
