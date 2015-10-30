#!/usr/bin/env python2.7
import os
from ansible.utils import module_docs

def generateExtra(required, choices):
    if len(choices) > 0:
        return ":#{0}".format("|".join(str(v) for v in choices))

    if required:
        return ":#REQUIRED"

    return ""

ansible_path = os.path.dirname(os.path.dirname(module_docs.__file__))
modules_path = os.path.join(ansible_path, 'modules')

for (dirpath, dirnames, filesname) in os.walk(modules_path):
    for f in filesname:
        if f.endswith('.py') and not f.startswith('__init__'):
            module = os.path.join(dirpath, f)
            docstring = module_docs.get_docstring(module)

            mod = docstring[0]
            if mod == None:
                continue

            name = mod['module']

            print "snippet\t\t{0}".format(name)
            print "options\t\thead"
            print "\t{0}:".format(name)

            # iterate module parameters
            paramIndex = 1
            for option in mod['options'].iteritems():
                parameters = option[1]
                required = parameters.get('required', False)
                choices  = parameters.get('choices', [])

                print "\t\t{option}: ${{{index}{extra}}}".format(
                    option=option[0],
                    index=paramIndex,
                    extra=generateExtra(required, choices))

                paramIndex +=1
            print "\n"
