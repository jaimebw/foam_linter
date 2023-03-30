# Foam Linter: A simple Open Foam linter
### WIP
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

WIP

