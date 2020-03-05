#!/usr/bin/python

#
# WARNING: Make changes wisely,     most of the change you do here have an impact on existing libraries publicly used
#          Make changes in cli too, most of the change you do here have an impact on rudder-cli
#

import jsonref
import re
import pprint
import urllib
from collections import OrderedDict

try:
    file = open("../openapi.json")
    data = jsonref.load(file, object_pairs_hook=OrderedDict)
    file.close()
except:
    file = open("../openapi.json", encoding='utf-8')
    data = jsonref.load(file, object_pairs_hook=OrderedDict)
    file.close()


def generate(url, method, description):
    # get method metadata
    name = convert(description['operationId'])
    method = method.upper()
    url = "/api" + url
    title = description['summary']

    url_params = []
    mandatory_params = []
    optional_params = []

    # get parameters metadata
    if 'parameters' in description:
        for parameter in description['parameters']:
            if parameter['in'] == "path":
                url_params.append(parameter['name'])
            # FIXME body parameters are in specific containers
            elif 'required' in parameter and parameter['required']:
                mandatory_params.append(parameter['name'])
            else:
                optional_params.append(parameter['name'])

    parameters = url_params + mandatory_params
    if method != 'GET':
        parameters.append("change_info=None")
    parameters.extend([x+'=None' for x in optional_params])

    # write method code
    print('  def ' + name +
          '(' + ', '.join(['self'] + parameters + ['return_raw=False']) + '):')
    print('    """ ' + title + ' (' + method.lower() + ') """')
    if method == 'PUT' or method == 'POST':
        print('    data = { ')
        for param in mandatory_params:
            print('            "' + param + '": ' + param + ",")
        for param in optional_params:
            print('            "' + param + '": ' + param + ",")
        print('           }')
        print('    clean_params(data)')
    final_url = '"' + url.replace('{', '" + ').replace('}', ' + "') + '"'
    if method == 'GET':
        print('    extra=""')
        for param in optional_params:
            print("    if %s is not None:" % (param))
            print('      extra += "?%s=" + urllib.parse.quote(%s)' %
                  (param, param))
        print('    if extra != "": final_url += "/" + extra')
        print('    return self.request("' + method + '", ' +
              final_url + ' + extra, return_raw=return_raw)')
    elif method == 'DELETE':
        print('    return self.request("' + method + '", ' +
              final_url + ', change_info, return_raw=return_raw)')
    else:
        print('    return self.request("' + method + '", ' +
              final_url + ', change_info, data, return_raw=return_raw)')
    print('')


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == "__main__":
    print('')
    for url in data['paths']:
        for method in data['paths'][url]:
            generate(url, method, data['paths'][url][method])
