import os
import glob
from oelint_adv.cls_stash import Stash
from oelint_adv.cls_item import Comment, Function, Include, Item, PythonBlock, Variable
from urllib.parse import urlparse

def get_files(stash, _file, pattern):
    res = []
    src_uris = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                 attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
    files_paths = list(
        set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern) for x in src_uris]))
    for item in src_uris:
        files_paths += list(set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern)
                                 for x in stash.GetItemsFor(filename=item.Origin)]))
    for item in files_paths:
        res += glob.glob(item)
    return list(set(res))

def get_scr_components(string):
    """ 
        Parses an URL string
        returns a dict with
            scheme = protcol used
            src = path to call
            options = dict with options added to URL
    """
    _url = urlparse(string)
    _scheme = _url.scheme
    _options = _url.netloc.split(";")[1:]
    _path = _url.netloc.split(";")[0]
    if _url.path:
        if not _path.endswith("/") and not _url.path.startswith("/"):
            _path += "/"
        _path += _url.path
    _parsed_opt = {x.split("=")[0]:x.split("=")[1] for x in _options}
    return {"scheme": _scheme, "src": _path, "options": _parsed_opt}