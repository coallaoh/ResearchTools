__author__ = "joon"

import pprint
import platform
import os
import os.path as osp


class filemanager(object):
    def __init__(self, maindir, filename):
        self.maindir = maindir
        self.filename = filename


class experiment_control(object):
    def __init__(self, control, conf, default, exclude=()):
        self.conf = conf
        self.control = control
        self._default = default
        self._exclude = exclude
        self.control_token = self._apply_defaults(self.control, self._default)
        self._apply_excludes(self.control_token, self._exclude)
        from util.construct_filenames import create_token
        self.token = create_token(self.control_token)
        self._set_maindir()

    def filemanager(self, filename, pathname, override=False):
        path = osp.join(self.maindir, filename)
        if not (self.conf['overridecache'] or override):
            if osp.isfile(path):
                from util.exceptions import CacheFileExists
                raise CacheFileExists("File %s already exists!" % path)
        self.dirs[pathname] = path

    def _set_maindir(self):
        self.maindir = osp.join('cache', self.conf['exp_phase'], self.token)
        from util.ios import mkdir_if_missing
        mkdir_if_missing(self.maindir)
        self.dirs = {}

    def _apply_defaults(self, control, default_control):
        import copy
        control_token = copy.deepcopy(control)
        for ky in default_control:
            if ky in control_token.keys():
                if isinstance(control_token[ky], dict):
                    assert (isinstance(default_control[ky], dict))
                    if control_token[ky] == default_control[ky]:
                        control_token.pop(ky)
                    else:
                        subcontroltoken = self._apply_defaults(control_token[ky], default_control[ky])
                        control_token[ky] = subcontroltoken
                else:
                    if control_token[ky] == default_control[ky]:
                        control_token.pop(ky)

        return control_token

    def _apply_excludes(self, control, exclude):
        for ex in exclude:
            ky = ex['condition'].keys()[0]
            if control[ky] == ex['condition'][ky]:
                control.pop(ex['remove'])

    def _print(self):
        print(":" * 50)
        print("Machine : %s" % platform.node())
        print("GPU : %d" % self.conf['gpu'])
        print("PID : %d" % os.getpid())
        print(">>> Exp Name <<<")
        print(self.conf['exp_phase'])
        print(">>> Conf <<<")
        pprint.pprint(self.conf)
        print(">>> Control <<<")
        pprint.pprint(self.control)
        print("Token : %s" % self.token)
        print(":" * 50)
        return

    def __enter__(self):
        self._print()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._print()
