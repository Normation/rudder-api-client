#!/usr/bin/python

import json
import re
import pprint

file=open("api_data.json")
data=json.load(file)
file.close()


def generate(function):
  # get method metadata
  name   = convert(function['name'])
  method = function['type'].upper()
  url    = function['url']

  url_params = []
  mandatory_params = []
  optional_params = []
  
  # get parameters metadata
  if 'parameter' in function:
    parameter_list = function['parameter']['fields']
    for plist in parameter_list.itervalues():
      for parameter in plist:
        if parameter['group'] == "URL parameters":
          url_params.append(parameter['field']);
        elif parameter['optional']:
          optional_params.append(parameter['field']);
        else:
          mandatory_params.append(parameter['field']);

  parameters = url_params + mandatory_params
  if method != 'GET':
    parameters.append("change_info=None")
  parameters.extend([x+'=None' for x in optional_params])

  # write method code
  print('  def ' + name + '(' + ', '.join(['self'] + parameters) + '):')
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
    print('    return self.request("' + method + '", ' + final_url + ')')
  elif method == 'DELETE':
    print('    return self.request("' + method + '", ' + final_url + ', change_info)')
  else:
    print('    return self.request("' + method + '", ' + final_url + ', change_info, data)')
  print('')


def convert(name):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if __name__ == "__main__":
  print('')
  for fct in data:
    generate(fct)


