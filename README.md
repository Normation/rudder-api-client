Command line interface for Rudder API
=====================================

Clients and libraries to call rudder

Synopsis
--------

    rudder-cli nodes list --skip-verify
    rudder-cli group list --skip-verify
    rudder-cli group show 9a07de69-6c52-4f54-9525-06acd6d0edc4
    rudder-cli api GET /api/nodes
    rudder-cli node list_pending | jq '.nodes[0]'


Installation
------------
This is a preview code, you need to install it from github at the moment.

    pip install -r requirements.txt

Clone the repository, then run:

    cd lib.python && ./build.sh

And put this script in /usr/local/bin/rudder-cli

    #!/bin/sh
    BASE=<your_repo_path>
    PYTHONPATH=${BASE}/lib.python
    export PYTHONPATH
    ${BASE}/cli/rudder-cli "$@"

Then create a Rudder API token from Rudder Administration menu > API Accounts

It is a good idea to put all your default arguments in a configuration file in ~/.rudder

    [default]
    token=AZERTYUIOP
    url=https://myhost.example.com/rudder
    skip-verify

Documentation
-------------

Use either rudder-cli --help or rudder-cli \<something> --help to get details on command line arguments.

    A CLI interface the Rudder Web API.

    Usage:
      rudder-cli api <method> <api_url> [options]
      rudder-cli ( rule | rules ) [<args>...] [options]
      rudder-cli ( change-request | change-requests ) [<args>...] [options]
      rudder-cli ( node | nodes ) [<args>...] [options]
      rudder-cli ( directive | directives ) [<args>...] [options]
      rudder-cli ( group | groups ) [<args>...] [options]

    Options:
     -h --help                Show help
     -f --conffile=<file>     Configuration file (default: ~/.rudder)
     -u --url=<url>           Base URL (default: https://localhost/rudder)
     -t --token=<token>       API token (create one from Rudder administration)
     -a --ca=<file>           Certificate authority to use to verify SSL (default: python CA bundle)
     --skip-verify            To avoid SSL certificate verification
     -p --proxy=<proxy>       Proxy to use to connect to api (default: '')
     --timeout=<timeout>      Timeout default duration in seconds (default: 5s)
     -r --raw                 Print raw answer
     --reason=<reason>        Reason message for changes (default '')
     --cr-name=<name>         Change Request name (default defined in Rudder)
     --cr-description=<text>  Change Request description
     -j --json=<file>         Add a json input (can be used instead of optional parameters, defaults to stdin for direct api call)



Since we are talking about manipulating json in command line, I warmly recommend you to take a look at jq http://stedolan.github.io/jq/
For example, to get the first pending node:

    rudder-cli node list_pending | jq '.nodes[0]'

To get the hostname of all pending nodes:

    rudder-cli node list_pending | jq '.nodes[].hostname'



Python library for Rudder API
=============================

Synopsis
--------

    from rudder import RudderEndPoint
    endpoint = RudderEndPoint("https://localhost/rudder", "123465789")
    nodes = endpoint.list_accepted_nodes()
    details = endpoint.accepted_node_details("0123465798")

This API is a basic mapping on Rudder REST API http://www.rudder-project.org/rudder-api-doc/
To call it, just create a Rudder endpoint, it will contain all methods of the Rudder API.

Constructor and caller
----------------------

    class rudder.RudderEndPoint(endpoint_url, api_key, version='latest', timeout=5, verify=True, proxy=None)

Endpoint constructor

    request(self, method, api_url, change_info=None, data=None, json_data=None, return_raw=False)

Generic API call, use this when there is a function that has no method in this API yet.
This method is called internally by all other methods.

API methods
-----------

    accept_change_request(self, id, status, change_info=None, return_raw=False)
Accept a Change Request (post)
  
    accepted_node_details(self, id, include=None, return_raw=False)
Get Node details (get)
  
    change_node_status(self, id, status, change_info=None, return_raw=False)
Change pending Node status (post)
  
    change_request_details(self, id, return_raw=False)
Get a Change Request details (get)
  
    clone_directive(self, source, displayName, change_info=None, parameters=None, shortescription=None, longDescription=None, id=None, enabled=None, priority=None, techniqueVersion=None, return_raw=False)
Clone a Directive (put)
  
    clone_group(self, source, displayName, change_info=None, description=None, dynamic=None, query=None, id=None, enabled=None, return_raw=False)
Clone a Group (put)
  
    clone_rule(self, source, displayName, change_info=None, id=None, shortDescription=None, longDescription=None, enabled=None, directives=None, targets=None, return_raw=False)
Clone a Rule (put)
  
    create_directive(self, techniqueName, displayName, change_info=None, parameters=None, shortDescription=None, longDescription=None, id=None, enabled=None, techniqueVersion=None, return_raw=False)
Create a new Directive (put)
  
    create_group(self, nodeGroupCategory, displayName, change_info=None, description=None, dynamic=None, query=None, id=None, enabled=None, return_raw=False)
Create a new Group (put)
  
    create_rule(self, displayName, change_info=None, id=None, shortDescription=None, longDescription=None, enabled=None, directives=None, targets=None, return_raw=False)
Create a new Rule (put)
  
    decline_change_request(self, id, change_info=None, return_raw=False)
Decline a Change Request (delete)
  
    delete_directive(self, id, change_info=None, return_raw=False)
Delete a Directive (delete)
  
    delete_group(self, id, change_info=None, return_raw=False)
Delete a Group (delete)
  
    delete_node(self, id, change_info=None, return_raw=False)
Delete Node (delete)
  
    delete_rule(self, id, change_info=None, return_raw=False)
Delete a Rule (delete)
  
    directive_details(self, id, return_raw=False)
Get a Directive details (get)
  
    group_details(self, id, return_raw=False)
Get Group details (get)
  
    list_accepted_nodes(self, return_raw=False)
List accepted Nodes (get)
  
    list_change_requests(self, status=None, return_raw=False)
List all Changes Requests (get)
  
    list_directives(self, return_raw=False)
List all Directives (get)
  
    list_groups(self, return_raw=False)
List all Groups (get)
  
    list_pending_nodes(self, return_raw=False)
List pending Nodes (get)
  
    list_rules(self, return_raw=False)
List all Rules (get)
  
    reload_group(self, id, change_info=None, return_raw=False)
Reload a Group (post)
  
    rule_details(self, id, return_raw=False)
Get a Rule details (get)
  
    update_change_request(self, id, change_info=None, name=None, description=None, return_raw=False)
Update a Change Request (post)
  
    update_directive(self, id, change_info=None, displayName=None, shortDescription=None, longDescription=None, parameters=None, enabled=None, priority=None, techniqueVersion=None, return_raw=False)
Update a Directive (post)
  
    update_group(self, id, change_info=None, displayName=None, description=None, dynamic=None, query=None, enabled=None, return_raw=False)
Update a Group (post)
  
    update_node_properties(self, id, change_info=None, return_raw=False)
Set Node properties (post)
  
    update_rule(self, id, change_info=None, displayName=None, enabled=None, shortDescription=None, longDescription=None, directives=None, targets=None, return_raw=False)
Update a Rule (post)

