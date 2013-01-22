# -*- coding: utf-8 -*-

import types

def call(target, name, *args):
    try:
        method = getattr(target, name)
        return method(*args)
    except:
        pass
