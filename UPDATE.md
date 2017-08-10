Updating api_data.json
======================

The file api_data.json is used to build the python api library.
This file comes from the rudder-api-doc repository.

To update to the last version, checkout rudder-api-doc, build the doc, then you can find the file in ./generated_doc/api_data.json
It is also available on jenkins in /var/lib/jenkins/jobs/rudder-api-doc/workspace/generated_doc/api_data.json

Then run build.sh and check that the cli can still run.


