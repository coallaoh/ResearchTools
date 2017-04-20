__author__ = "joon"

def subcontrol(control, token):
    control_sub = dict()
    kys = control.keys()
    for ky in kys:
        if ky[:2] == token + '_':
            control_sub[ky[2:]] = control[ky]

    return control_sub


