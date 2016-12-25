
import os

class _EnvArg(object):
    def __init__(self, envnamesuf):
        self._envname = 'MKENUMSTR_CLIARG__' + envnamesuf

    def set(self, v):
        if v is None and self._envname in os.environ:
            del os.environ[self._envname]
        else:
            os.environ[self._envname] = str(v)

    def get(self):
        if self._envname in os.environ:
            v = os.environ[self._envname]
            return v if v != 'None' else None
        else:
            return None

ohfile = _EnvArg('OHFILE')
ocfile = _EnvArg('OCFILE')
symbfile = _EnvArg('SYMBFILE')
