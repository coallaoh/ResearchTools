__author__ = "joon"

import pprint
import platform
import os
import os.path as osp
import copy
from util.construct_filenames import create_token


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
        self._clean_token(self.control_token)
        self.token = create_token(self.control_token)
        self._set_maindir()

    def update_token(self):
        self.control_token = self._apply_defaults(self.control, self._default)
        self._apply_excludes(self.control_token, self._exclude)
        self._clean_token(self.control_token)
        self.token = create_token(self.control_token)

    def _clean_token(self, control_token):
        for ky in control_token.keys():
            subct = control_token[ky]
            if isinstance(subct, dict):
                if len(subct) == 0:
                    control_token.pop(ky)
                else:
                    self._clean_token(subct)

    def filemanager(self, filename, pathname, override=False, ignore=(), assert_exist=False):
        if len(ignore) == 0:
            path = osp.join(self.maindir, filename)
        else:
            ct = copy.deepcopy(self.control_token)
            for ig in ignore:
                self._remove_item(ct, ig.split('/'))
            self._clean_token(ct)
            path = osp.join('cache', self.conf['exp_phase'], create_token(ct), filename)

        if not (self.conf['overridecache'] or override):
            if osp.isfile(path):
                from util.exceptions import CacheFileExists
                raise CacheFileExists("File %s already exists!" % path)
        self.dirs[pathname] = path
        if assert_exist:
            assert (osp.isfile(path))

    def _set_maindir(self):
        self.maindir = osp.join('cache', self.conf['exp_phase'], self.token)
        from util.ios import mkdir_if_missing
        mkdir_if_missing(self.maindir)
        self.dirs = {}

    def _apply_defaults(self, control, default_control):
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

    def _remove_item(self, obj, removeloc):
        if removeloc[0] not in obj.keys():
            return
        if len(removeloc) == 1:
            if removeloc[0] in obj.keys():
                obj.pop(removeloc[0])
        else:
            self._remove_item(obj[removeloc[0]], removeloc[1:])

    def _get_attr(self, ct, attr):
        if isinstance(ct[attr[0]], dict):
            return self._get_attr(ct[attr[0]], attr[1:])
        else:
            return ct[attr[0]]

    def _apply_excludes(self, control, exclude):
        for ex in exclude:
            if 'condition' in ex.keys():
                ky = list(ex['condition'].keys())[0]
                control_attr = self._get_attr(self.control, ky.split('/'))
                if control_attr == ex['condition'][ky]:
                    self._remove_item(control, ex['remove'].split('/'))
            else:
                self._remove_item(control, ex['remove'].split('/'))

    def _print(self):
        print(":" * 50)
        print("Machine : %s" % platform.node())
        print("GPU : {}".format(self.conf['gpu']))
        print("PID : %d" % os.getpid())
        print(">>> Exp Name <<<")
        print(self.conf['exp_phase'])
        # print(">>> Conf <<<")
        # pprint.pprint(self.conf)
        print(">>> Control <<<")
        pprint.pprint(self.control)
        print("Token : %s" % self.token)
        print(":" * 50)
        return

    def __enter__(self):
        self._print()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._print()
