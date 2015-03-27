# -*- coding: utf-8 -*-
"""
    fiddlersgreen.compat
    ~~~~~~~~~~~~~~~~~

    Python 2/3 compatibility module.

"""
import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    text_type = unicode  # NOQA
    binary_type = str  # NOQA
    string_types = (str, unicode)  # NOQA
    unicode = unicode  # NOQA
    basestring = basestring  # NOQA
else:
    text_type = str  # NOQA
    binary_types = bytes  # NOQA
    string_types = (str,)  # NOQA
    unicode = str  # NOQA
    basestring = (str, bytes)  # NOQA
