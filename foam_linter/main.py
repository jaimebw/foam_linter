import re
from pathlib import Path
from typing import Dict, Tuple
from enum import Enum


class DictionaryType(Enum):
    controlDict = 1
    blockMeshDict = 2
    decomposeParDict = 3 


class FoamLinter:
    def __init__(self,data:str)->None:
        self.data = data
        self.info = dict()
        self.errors = dict()
        self.__get_object_class()
        self.__get_file_type()

    
    def __get_object_class(self)->None:
        """
        Get the file class
        """
        class_pattern = r'class\s+(\w+);'
        class_match = re.search(class_pattern, self.data)
        if class_match:
            class_value = class_match.group(1)
        else:
            class_value = None
        self.info["dict_class"] = class_value
        

    def __get_file_type(self)->None:
        """
        Get the file type
        """
        object_pattern = r'object\s+(\w+);'
        object_match = re.search(object_pattern, self.data)
        if object_match:
            object_value = object_match.group(1)
        else:
            object_value = None
        self.info["dict_type"] = object_value

    def check_brackets(self)->bool:
        """
        Check if the brackets of the file are closed.
        """
        stack = []
        for c in self.data:
            if c in '([{':
                stack.append(c)
            elif c in ')]}':
                if not stack:
                    return False
                top = stack.pop()
                if (c == ')' and top != '(') or \
                   (c == ']' and top != '[') or \
                   (c == '}' and top != '{'):
                    return False
        return not stack
    
    def lint(self)->Tuple[dict[str,str],bool]:
        """
        It willl lint the dictionary depending on the type of the dict.

        """

        if not self.check_brackets:
            self.errors["closed_brackets"] = True
        else:
            self.errors["closed_brackets"] = False
            return (self.errors,1)

        type_val = DictionaryType(self.info["dict_type"]).value 

        if type_val == 1:
            errors, error_code = self.controlDict_linter(self.data)    
            errors= errors| self.errors
            return (errors,error_code)
        elif type_val == 2:
            errors, error_code = self.blockMeshDict_linter(self.data)    
            errors= errors| self.errors
            return (errors,error_code)
        else:
            # TO_DO: add more cases to de linter
            pass
    @staticmethod
    def controlDict_linter(data:str)->Tuple[dict[str,str],bool]:
        """
        A simple linter for the controlDict file of OpenFoam
        """
        errors = dict()
        keywords = [
        "application",
        "startFrom",
        "startTime",
        "stopAt",
        "endTime",
        "deltaT",
        "writeControl",
        "writeInterval",
        "purgeWrite",
        "writeFormat",
        "writePrecision",
        "writeCompression",
        "timeFormat",
        "timePrecision",
        "runTimeModifiable"]
        # Find the first closing brace and start parsing after it
        start_idx = data.find("}") + 1
        content = data[start_idx:]
        missing_keywords = []
        for keyword in keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        errors["controlDict_linter"] = missing_keywords
        if missing_keywords:
            return errors, 1
        else:
            return errors, 0


    @staticmethod
    def blockMeshDict_linter(data:str)->Tuple[dict[str,str],bool]:
        """
        A simple linter for the blockMeshDict file of OpenFoam
        """
        errors = dict()
        keywords = [
            "scale",
            "rInner",
            "rOuter",
            "xmax",
            "ymax",
            "zmin",
            "zmax",
            "nRadial",
            "nQuarter",
            "nxOuter",
            "nyOuter",
            "nz",
            "vertices",
            "pointField",
            "points",
            "blocks",
            "hex",
            "grading",
            "edges",
            "arc",
            "origin",
            "boundary",
            "type",
            "symmetryPlane",
            "faces",
            "patch",
            "symmetry",
            "mergePatchPairs"
            ]
        # Find the first closing brace and start parsing after it
        start_idx = data.find("}") + 1
        content = data[start_idx:]
        missing_keywords = []
        for keyword in keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        errors["blockMeshDict_linter"] = missing_keywords
        if missing_keywords:
            return errors, 1
        else:
            return errors, 0

    @staticmethod
    def decomposeParDict_linter(data:str)->Tuple[dict[str,str],bool]:
        """
        A simple linter for the blockMeshDict file of OpenFoam
        """
        errors = dict()
        keywords = [
            "numberOfSubdomains",
            "method",
            "simple",
            "coeffs",
            "n"
            ]
        # Find the first closing brace and start parsing after it
        start_idx = data.find("}") + 1
        content = data[start_idx:]
        missing_keywords = []
        for keyword in keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        errors["decomposeParDict_linter"] = missing_keywords
        if missing_keywords:
            return errors, 1
        else:
            return errors, 0


    @staticmethod
    def remove_comments():
        """
        TO_DO
        Deletes the comments in the file

        """
        pass


