from __future__ import annotations
from typing import Dict, List, Tuple, Union

import json


class JsonClass:
    json_attributes: Tuple[str] = ()

    @classmethod
    def alltypes(cls) -> Dict[str, JsonClass]:
        retVal = {}
        for i in cls.__subclasses__():
            retVal[i.__name__] = i
        return retVal

    def save_dict(self):
        return make_dict(self, self.json_attributes)

    def save_json_string(self, indent=4, **kwargs):
        return json.dumps(self.save_dict(), indent=indent, **kwargs)

    def save_json_file(self, filepath: str, indent=4, **kwargs):
        return json.dump(self.save_dict(), open(filepath, "w"), indent=indent, **kwargs)

    def load_json_file(self, filepath: str):
        in_data = json.load(open(filepath, "r"))
        self.load_dict(in_data)

    def load_json_string(self, p_str: str):
        in_data = json.loads(p_str)
        self.load_dict(in_data)

    def load_dict(self, p_dict: Dict[str, object]):

        json_classes = self.alltypes()
        for key, value in p_dict.items():

            if key.startswith("-"):
                type_info = key.split("-")[1:]
                new_obj = json_classes[type_info[0]]()
                new_obj.load_dict(value)
                setattr(self, type_info[1], new_obj)
            else:
                setattr(self, key, value)

    def load(self, **p_dict):
        self.load_dict(p_dict)

    @classmethod
    def new_from_string(cls, p_data: dict):
        retVal = cls()
        retVal.load_json_string(p_data)
        return retVal

    @classmethod
    def new_from_file(cls, p_data: dict):
        retVal = cls()
        retVal.load_json_file(p_data)
        return retVal

    @classmethod
    def new_from_dict(cls, p_data: dict):
        retVal = cls()
        retVal.load_dict(p_data)
        return retVal

    @classmethod
    def new(cls, **p_data):
        retVal = cls()
        retVal.load(**p_data)
        return retVal


def make_dict(obj, attrs: Union[List[str], Tuple[str]]):
    retVal = {}
    for i in attrs:
        if hasattr(obj, i):
            attr = getattr(obj, i)
            if isinstance(attr, JsonClass):
                typename = type(attr).__name__
                retVal[f"-{typename}-{i}"] = attr.save_dict()
            else:
                retVal[i] = attr
        else:
            pass
            # print(f"ERROR: object '{str(obj)}' does not have attribute '{i}'...")

    return retVal
