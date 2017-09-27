__author__ = "joon"

import pprint
import platform
import os


class experiment_control(object):
    def __init__(self, control, conf, default):
        self.conf = conf
        self.control = control
        self._default = default
        self.control_token = self._apply_defaults(self.control, self._default)
        from util.construct_filenames import create_token
        self.token = create_token(self.control_token)

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

    def _print(self):
        print(":" * 50)
        print("Machine : %s" % platform.node())
        print("GPU : %d" % self.conf['gpu'])
        print("PID : %d" % os.getpid())
        print(">>> Control <<<")
        pprint.pprint(self.control)
        print("Token : %s" % self.token)
        print(":" * 50)
        return

    def __enter__(self):
        self._print()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._print()
