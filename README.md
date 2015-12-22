# Introduction

A really simple web app to generate and send simple netconf GET requests and to generate a sample Python script that uses ncclient.

# Installation

Installation on ADS servers is not possible right now due to libxml2 dependencies that are not currently satisfied. Also, if you wish to talk to an IOS-XR box, which mandates ```netconf:base:1.1```, you will currently need to install a special version of ncclient that resides at:

https://github.com/einarnn/ncclient

Once pull request #98 on the main ncclient repository has been merged, you **should** be able to use the core distribution of ncclient.

If you don't need to talk to XR, then running the start script ([```start.sh```](start.sh)) should be adequate. If, however, you do wish to access XR, then this is the basic process tested on _**a mac running El Capitan with homebrew utilities**_:

```
16:34 $ git clone http://gitlab.cisco.com/einarnn/flask-netconf.git
Cloning into 'flask-netconf'...
remote: Counting objects: 36, done.
remote: Compressing objects: 100% (33/33), done.
remote: Total 36 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (36/36), done.
Checking connectivity... done.
16:34 $ cd flask-netconf
16:34 $ virtualenv v
New python executable in v/bin/python2.7
Also creating executable in v/bin/python
Installing setuptools, pip, wheel...
done.
16:35 $ source v/bin/activate
16:35 $ pip install lxml==3.4.4
Collecting lxml==3.4.4
Installing collected packages: lxml
Successfully installed lxml-3.4.4
16:35 $ cd ..
16:35 $ git clone https://github.com/einarnn/ncclient
Cloning into 'ncclient'...
remote: Counting objects: 3016, done.
remote: Total 3016 (delta 0), reused 0 (delta 0), pack-reused 3016
Receiving objects: 100% (3016/3016), 2.53 MiB | 435.00 KiB/s, done.
Resolving deltas: 100% (1620/1620), done.
Checking connectivity... done.
16:35 $ cd ncclient
16:35 $ python setup.py install
running install
running bdist_egg
running egg_info
creating ncclient.egg-info
writing requirements to ncclient.egg-info/requires.txt

[...many details elided...]

Using /Users/einarnn/scratch/foo/flask-netconf/v/lib/python2.7/site-packages
Finished processing dependencies for ncclient==0.4.6
16:36 $ cd ../flask-netconf
16:36 $ ./start.sh
virtual env already created
Requirement already satisfied (use --upgrade to upgrade): ecdsa==0.13 in ./v/lib/python2.7/site-packages/

[...many details elided...]

Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.3 itsdangerous-0.24
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

At this point you may open the link [http://127.0.0.1:5000/netconf](http://127.0.0.1:5000/netconf)!

## Q&A

* Why install ```lxml==3.4.4``` explicitly above?
    * This may not be necessary in your environment. ```lxml``` is required by ```ncclient```, and on a mac the last good version is 3.4.4, so install that manually first if you're installing the private version of ncclient.