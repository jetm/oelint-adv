import glob
import importlib
import inspect
import os
import pkgutil

from oelint_adv.cls_item import *

class Rule():
    def __init__(self, id="", severity="", message=""):
        self.ID = id
        self.Severity = severity
        self.Msg = message

    def check(self, _file, stash):
        return []

    def fix(self, _file, stash):
        return []

    def finding(self, _file, _line, override_msg=None):
        return ["{}:{}:{}:{}:{}".format(os.path.abspath(_file), _line, self.Severity, self.ID, override_msg or self.Msg)]

    def __repr__(self):
        return "{}".format(self.ID)

    def FormatMsg(self, *args):
        return self.Msg.format(*args)

    def OverrideMsg(self, newmsg):
        self.Msg = newmsg


def load_rules(add_rules=[]):
    res = []
    _path_list = {
        "base": os.path.dirname(os.path.abspath(__file__))
    }
    for ar in add_rules:
        _path_list[ar] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rule_{}".format(ar))
    for k,v in _path_list.items():
        packages = pkgutil.walk_packages(path=[v])
        for importer, name, is_package in packages:
            if k != "base":
                name = os.path.basename(v) + "." + name
            mod = importlib.import_module(name)
            for m in inspect.getmembers(mod, inspect.isclass):
                try:
                    if issubclass(m[1], Rule):
                        inst = m[1]()
                        if inst.ID:
                            res.append(inst)
                except Exception as ex:
                    print("{} -> {}".format(name, ex))
    return res
