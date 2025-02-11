from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
from oelint_adv.const_func import FUNC_ORDER
from anytree import Node, LoopError, TreeError, RenderTree
import os
import re


class TaskCustomOrder(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.customorder",
                         severity="error",
                         message="<FOO>")

    def __getNodeFromException(self, msg):
        m = re.match(r"^.*Node\(\'(?P<path>.*)\'\)\.$", msg)
        if m:
            return [x for x in m.group("path").split("/") if x]
        return []

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=TaskAdd.CLASSIFIER)
        _nodes = []
        for item in items:
            for t in item.After:
                _n = None
                _m = None
                try:
                    _t = [y for y in _nodes if y.name == t]
                    if not any(_t):
                        _n = Node(t)
                        _nodes.append(_n)
                    else:
                        _n = _t[0]
                    _t = [y for y in _nodes if y.name == item.FuncName]
                    if not any(_t):
                        _m = Node(item.FuncName)
                        _nodes.append(_m)
                    else:
                        _m = _t[0]
                    if not _m in _n.children:
                        _n.children += (_m,)
                except LoopError as e:
                    _path = self.__getNodeFromException(str(e)) + [t]
                    self.OverrideMsg("Assignment creates a cyclic dependency - Path={}".format("->".join(_path)))
                    res += self.finding(item.Origin, item.InFileLine)
            for t in item.Before:
                try:
                    _n = None
                    _t = [y for y in _nodes if y.name == item.FuncName]
                    if not any(_t):
                        _n = Node(item.FuncName)
                        _nodes.append(_n)
                    else:
                        _n = _t[0]
                    _t = [y for y in _nodes if y.name == t]
                    _m = None
                    if not any(_t):
                        _m = Node(t)
                        _nodes.append(_m)
                    else:
                        _m = _t[0]
                    if not _m in _n.children:
                        _n.children += (_m,)
                except LoopError as e:
                    _path = self.__getNodeFromException(str(e)) + [t]
                    self.OverrideMsg("Assignment creates a cyclic dependency - Path={}".format("->".join(_path)))
                    res += self.finding(item.Origin, item.InFileLine)
        return res
