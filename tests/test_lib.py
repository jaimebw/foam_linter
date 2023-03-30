from foam_linter import *
from pathlib import Path

test_dir = Path("tests/test_files")

def load_data():
    
    with open(str(test_dir/"controlDict_badlyclosed"),"r") as f:
        data_badclosed = f.read()
    with open(str(test_dir/"controlDict"),"r") as f:
        data = f.read()
    return (data,data_badclosed)


def test_file_type():
    """
    Test for the getting the file type and the class type
    """
    data = load_data()[0]
    linter = FoamLinter(data)
    assert linter.info["dict_class"] == "dictionary"
    assert linter.info["dict_type"] == "controlDict"

def test_closed_brackets():
    data = load_data()
    #good_file = FoamLinter(data[0])
    bad_file = FoamLinter(data[1])

    assert bad_file.lint()[1] == 1
    
def test_controlDict_lint():
    """
    """
    data = load_data()[0]
    file_linter = FoamLinter(data)
    lint_results = file_linter.lint()
    print(lint_results[0])
    assert lint_results[1] == 1
    assert file_linter.info["dict_type"] == "controlDict"

    


