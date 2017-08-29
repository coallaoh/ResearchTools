__author__ = "joon"


def subcontrol(control, token):
    control_sub = dict()
    kys = control.keys()
    for ky in kys:
        if ky[:2] == token + '_':
            control_sub[ky[2:]] = control[ky]

    return control_sub


def defaults(control, defaults_control):
    import copy
    control_token = copy.deepcopy(control)
    for ky in defaults_control:
        if ky in control_token.keys():
            if isinstance(control, dict):
                assert (isinstance(defaults_control, dict))
                if control_token[ky] == defaults_control[ky]:
                    control_token.pop(ky)
                else:
                    subcontroltoken = defaults(control_token[ky], defaults_control[ky])
                    control_token[ky] = subcontroltoken
            else:
                if control_token[ky] == defaults_control[ky]:
                    control_token.pop(ky)

    return control_token
