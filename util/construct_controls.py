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
            if isinstance(control_token[ky], dict):
                assert (isinstance(defaults_control[ky], dict))
                if control_token[ky] == defaults_control[ky]:
                    control_token.pop(ky)
                else:
                    subcontroltoken = defaults(control_token[ky], defaults_control[ky])
                    control_token[ky] = subcontroltoken
            else:
                if control_token[ky] == defaults_control[ky]:
                    control_token.pop(ky)

    return control_token


def apply_explist(control, exp_configs):
    # import copy
    for ky in exp_configs:
        assert (ky in control.keys())
        if isinstance(control[ky], dict):
            apply_explist(control[ky], exp_configs[ky])
        else:
            control[ky] = exp_configs[ky]
