# import the Flask class from the flask module
from flask import Flask, Markup, render_template, redirect, url_for, request
from jinja2 import Template
from lxml import etree
from ncclient import manager
from ncclient.operations import RPCError
from ncclient.transport import SSHError
import argparse
import snippets
import models
import json

# create the application object
app = Flask(__name__)

# A simple netconf session cache
session_cache = {}

# The default context for loaded models
context = None

# The data for jstree created at startup
jstreedata = None

#
# The Template Python Script for get requests
#
get_script_template=Template("""#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from ncclient import manager

data = '''<filter>
  {{FILL_THIS}}
</filter>'''
        
        
if __name__ == '__main__':

    parser = ArgumentParser(description='Select options.')

    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")
    
    args = parser.parse_args()

    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"csr"})
    print m.get(data)
""")

default_xml = '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yang-tree', methods=['GET', 'POST'])
def yang_tree():
    kw = {
        "JSTREEDATA": Markup(json.dumps(jstreedata))
    }
    return render_template('tree.html', **kw)

@app.route('/netconf-get', methods=['GET', 'POST'])
def netconf_get():
    kw = {
        "uri": "netconf-get",
        "OPER_GET": "checked",
        "snippets": snippets.get,
    }
    if request.method=='POST':
        for k,v in request.form.iteritems():
            if 'OPER' not in k:
                kw[k] = v
        if kw['submit']=='generate':
            kw['language'] = 'python'
            kw['response'] = get_script_template.render(FILL_THIS=kw['xml'])
        elif kw['submit']=='send':
            try:
                if not ('device_port' in kw):
                    kw['device_port'] = 830
                session_key = "-".join([kw['device_ip'],
                                        kw['device_port'],
                                        kw['username'],
                                        kw['password'] ])
                if session_key in session_cache:
                    m = session_cache[session_key]
                else:
                    m =  manager.connect(host=kw['device_ip'],
                                         port=int(kw['device_port']),
                                         username=kw['username'],
                                         password=kw['password'],
                                         device_params={'name':"csr"})
                    session_cache[session_key] = m
                c = m.get('<filter>'+kw['xml']+'</filter>').data_xml
                kw['language'] = 'xml'
                kw['response'] = etree.tostring(etree.fromstring(c), pretty_print=True)
            except RPCError as e:
                kw['response'] = e.info
            except SSHError as e:
                kw['response'] = e.message
            except:
                kw['response'] = 'Unknown error!!'
    else:
        kw['xml'] = default_xml
    return render_template('code-generator.html', **kw)  # render a template


@app.route('/netconf-get-config', methods=['GET', 'POST'])
def netconf_get_config():
    kw = {
        "uri": "netconf-get-config",
        "operation": "get-config",
        "snippets": snippets.get_config,
        "example": '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <link-up-down-trap-enable/>
  </interface>
</interfaces>'''
    }
    return render_template('code-generator.html', **kw)  # render a template


@app.route('/netconf-edit-config', methods=['GET', 'POST'])
def netconf_edit_config():
    kw = {
        "uri": "netconf-edit-config",
        "operation": "edit-config",
        "snippets": snippets.edit_config,
        "example": "TBD"
    }
    return render_template('code-generator.html', **kw)  # render a template


# start the server with the 'run()' method
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Webapp to do stuff with netconf and yang!')
    parser.add_argument("--path", type=str, default="",
                        help="List of local directories to add to search path.")
    parser.add_argument("--models", nargs='+',
                        help="List of local directories to add to search path.")
    args = parser.parse_args()

    modules = None
    context = None
    if args.models:
        # parse in the list of models
        modules, context = models.load(args.path, args.models)

    if modules and context:
        # just dump some stuff out for now
        # print('Context Modules:')
        # for (m, r) in context.modules:
        #     print("  {}, revision {}".format(m, r))
        # print('Added Modules:')
        # for m in modules:
        #     print("  {}".format(m.i_modulename))
        #     def print_child(stmt, n):
        #         fmt = n * "  " + "{}:{}"
        #         print(fmt.format(stmt.i_module.i_prefix, stmt.arg))
        #         if not hasattr(stmt, "i_children"):
        #             return
        #         for child in stmt.i_children:
        #             print_child(child, n+1)
        #     for stmt in m.i_children:
        #         print_child(stmt, 2)

        jstreedata = models.create_jstreedata(modules, context)

    app.run(host="0.0.0.0", port=8000, debug=True)
