from pdb import set_trace as st
import numpy as np
import types
import sys


def create_token(a):
    if not a:
        return ''

    keyvalues = a.keys()

    names = []

    for key in keyvalues:

        category = key
        value = a[key];

        if sys.version[0] == '3':

            if type(value) == bool:
                if value:
                    name = category
                else:
                    continue
            elif type(value) == type(None):
                name = category + ':' + 'None'
            elif type(value) == int:
                name = category + ':' + str(value)
            elif type(value) == float:
                name = category + ':' + str(value)
            elif type(value) == np.ndarray:
                name = category + ':' + str(value)
            elif type(value) == str:
                name = category + ':' + value
            elif type(value) == bytes:
                name = category + ':' + value
            elif type(value) == list:
                name = category + ':' + str(value)
            elif type(value) == dict:
                name = category + ':' + '(' + create_token(value) + ')'
            else:
                print ("create_token: take care of the case for type " + str(type(value)))

        else:

            if type(value) == types.BooleanType:
                if value:
                    name = category
                else:
                    continue
            elif type(value) == types.NoneType:
                name = category + ':' + 'None'
            elif type(value) == types.IntType:
                name = category + ':' + str(value)
            elif type(value) == types.FloatType:
                name = category + ':' + str(value)
            elif type(value) == np.ndarray:
                name = category + ':' + str(value)
            elif type(value) == types.StringType:
                name = category + ':' + value
            elif type(value) == types.ListType:
                name = category + ':' + str(value)
            elif type(value) == types.DictionaryType:
                name = category + ':' + '(' + create_token(value) + ')'
            else:
                print ("create_token: take care of the case for type " + str(type(value)))

        names.append(name)

    names.sort()

    output = ''

    for name in names:
        output = output + '_' + name

    return output
