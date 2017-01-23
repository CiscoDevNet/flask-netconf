# Introduction

A really simple web app to generate and send simple netconf GET requests and to generate a sample Python script that uses ncclient.

# Installation

Please run the script ```start.sh```. This will create a virtualenv, attempt to load required dependencies, and start the web application. Note that the dependencies may require native libraries to be installed in the underlyinging environment. Thes native library dependencies have not yet been fully documented.

Once the start.sh script has completed successfully, you may open the link [http://127.0.0.1:8080/netconf](http://127.0.0.1:8080/netconf)!

Please note that this web application has no security as part of its function, but neither does it cache credentials, and any device communication requires the end-user to provide credentials.
