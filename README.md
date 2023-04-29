# Foam Linter: A simple Open Foam linter
Linting and checking for OpenFoam files. At the moment, partial functionality is only suported for:
* decomposeParDict
* controlDict
* blockMeshDict

## How to use
At the moment, this implementation only works by loading the files as strings.
Future iterations may change.

A simple example:
```python3
from foam_linter import FoamLinter

# file:str

linter = FoamLinter(file)
result = linter.lint()

result[0] # dictionary of errors
results[1] # error code, if 1 error if 0 no error
```

## How to install
I'll certanly upload it to PyPi in the future. At the moment, to install you need to:
```bash
git clone https://github.com/jaimebw/foam_linter.git 
cd foam_linter
pip install .
```


