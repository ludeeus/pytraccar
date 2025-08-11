# [pytraccar](https://pypi.org/project/pytraccar/)

[![codecov](https://codecov.io/gh/ludeeus/pytraccar/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/pytraccar)
![python version](https://img.shields.io/badge/Python-3.13-indigo.svg)
[![PyPI](https://img.shields.io/pypi/v/pytraccar)](https://pypi.org/project/pytraccar)


## Installation

```bash
python3 -m install pytraccar
```


## Usage

Look at the file `example.py` for a usage example.

`ApiClient` can be initialized as follows:

Required args:
* `host`: string hostname
* `token`: string, see [the API doc][api-doc] for details
* `client_session`: `aiohttp.ClientSession`; see example.py

Optional kwargs:
* `port`: integer, default `8082`
* `ssl`: boolean, default `False`
* `verify_ssl`: boolean, default `True`
* `ws_heartbeat`: integer, default `120`


## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `poetry run ruff check --fix pytraccar`
5. Format the files with `poetry run ruff format`
6. Ensure all tests passes and coverage is still at 100% with `poetry run pytest --cov`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch

[api-doc]: https://www.traccar.org/traccar-api/
