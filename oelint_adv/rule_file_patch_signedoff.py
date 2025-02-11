from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
from oelint_adv.helper_files import get_files
from urllib.parse import urlparse
import os


class FilePatchIsSignedOff(Rule):
    def __init__(self):
        super().__init__(id="oelint.file.patchsignedoff",
                         severity="warning",
                         message="Patch '{FILE}' should should contain a Signed-Off entry")

    def check(self, _file, stash):
        res = []
        items = get_files(stash, _file, "*.patch")
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in items:
            with open(i) as _input:
                content = _input.readlines()
                if not any([x for x in content if x.startswith("Signed-off-by: ")]):
                    # Find matching SRC_URI assignment
                    _assign = [x for x in _items if x.VarValue.find(
                        os.path.basename(i)) != -1]
                    if any(_assign):
                        self.OverrideMsg(self.Msg.replace(
                            "{FILE}", os.path.basename(i)))
                        res += self.finding(_assign[0].Origin,
                                            _assign[0].InFileLine)
        return res
