from oPOSum.apps.layaway.models import Layaway

def get_layaway_type(t):
    return next(ltype for ltype, code in Layaway.TYPES if code == t)
