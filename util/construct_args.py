__author__ = "joon"


def control2list(control):
    output = [] 
    for ky in control.keys():
        output.append("--" + ky)
        output.append(" " + str(control[ky]) + " ")
    return output




