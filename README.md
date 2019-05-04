# [pytraccar](https://pypi.org/project/pytraccar/)

Documentation for this package can be found here:  
[https://ludeeus.github.io/pytraccar/index.html](https://ludeeus.github.io/pytraccar/index.html)  


## Installation

```bash
python3 -m install pytraccar
```

## CLI test

```bash
traccar
```

Look at the file `example.py` for a usage example.


## Test

```bash
git clone https://github.com/ludeeus/pytraccar.git
cd pytraccar
python3 -m venv .
source bin/activate
python setup.py develop
```

change the content of `example.py` to match your IP, PORT, USERNAME and PASSWORD.

```bash
python example.py
```