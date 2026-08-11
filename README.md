openapi-eightball
=================

This is a toy REST service that acts like a digital magic eight ball
able to respond to one of a small fixed set of questions.

It is not safe, secure, or guaranteed to be functional for anything but the
specific queries it supports, and that is all. See the terms_of_use.html
file in this repository for more.

Start it by running, in a terminal window:
  python3 eightball.py
You will then be able to make queries to 127.0.1:8080 via a browser or curl.
Go to the url http://127.0.0.1:8080/8ball/v1/help for available queries.

If you want to run a second copy of it on another port, or a different host, you
may do so by running
  python3 eightball.py --host server-name-here --port port-number-here

If you would like to run the service over https instead of the default http,
you may do so by running
  python3 eightball.py --host server-name-here --port port-number-here
     --cert /full/path/to/cert/file --key /full/path/to/key/file
     
The toy service has an accompanying OpenAPI spec file. You will need to edit
it so that the servers: entry has the right urls for your service. This file
will be automatically served at http://127.0.0.1:8080/8ball/v1/openapi-spec.yaml
as well the terms of use file, via http://127.0.0.1:8080/8ball/v1/terms_of_use.html
or whatever hostname and port you specify as arguments when starting the service

This service is an example for use wth the MediaWiki Rest Sandbox,
see https://www.mediawiki.org/wiki/Help:RestSandbox for the Sandbox,
and https://www.mediawiki.org/wiki/Documentation/API_documentation/Registering_external_modules
for using this demo service and the included OpenAPI spec with
the Sandbox on a local installation of MediaWiki.
