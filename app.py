# import the Flask class from the flask module
from flask import Flask, Markup, render_template, redirect, url_for, request

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

import sys
from argparse import ArgumentParser
from ncclient import manager
from pythonTemplates import get_script_template, action


default_xml = '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>'''

op = {'get' : 'OPER_GET',
      'get_config' : 'OPER_GETCONFIG',
      'edit_config' : 'OPER_EDITCONFIG'}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yang-tree', methods=['GET', 'POST'])
def yang_tree():
    kw = {
        "JSTREEDATA": Markup(json.dumps(jstreedata))
    }
    return render_template('tree.html', **kw)


def get_connection(kw):
    if not ('device_port' in kw) or kw['device_port'] == "":
        kw['device_port'] = 830
    session_key = "-".join([kw['device_ip'],
                            kw['device_port'],
                            kw['username'],
                            kw['password']])
    if session_key in session_cache:
        m = session_cache[session_key]
    else:
        m = manager.connect(host=kw['device_ip'],
                            port=int(kw['device_port']),
                            username=kw['username'],
                            password=kw['password'],
                            look_for_keys=False,
                            hostkey_verify=False,
                            )
        session_cache[session_key] = m
    return m

@app.route('/netconf-op', methods=['GET', 'POST'])
def netconf_op():
    kw = {
        "snippets": snippets.snippets,
    }

    if request.method == 'POST':

        for k, v in request.form.iteritems():
            #if 'OPER' not in k:
            print k,v
            kw[k] = v
        kw[op[kw['oper']]] = 'checked'
        if kw['submit'] == 'generate':
            kw['language'] = 'python'
            kw['response'] = get_script_template.render(FILL_THIS=kw['xml'], ACTION=action[kw['oper']])
        elif kw['submit'] == 'send':
            m = None
            try:
                m = get_connection(kw)
            except RPCError as e:
                kw['response'] = e.info
            except SSHError as e:
                kw['response'] = e.message
            except KeyError as e:
                kw['resonse'] = e.message
            except:
                kw['response'] = 'Unknown error!!'
            if m is None:
                return render_template('code-generator.html', **kw)  # render a template for error

            if kw['oper'] == 'get':
                c = m.get('<filter>' + kw['xml'] + '</filter>').data_xml
                # print etree.tostring(etree.fromstring(c), pretty_print=True)
                kw['response'] = etree.tostring(etree.fromstring(c), pretty_print=True)

            elif kw['oper'] == 'get_config':
                c = m.get_config(source='running', filter=('subtree', kw['xml'])).data_xml
                kw['response'] = etree.tostring(etree.fromstring(c), pretty_print=True)

            elif kw['oper'] == "edit_config":
                c = m.edit_config(kw['xml'], target='running', format='xml',default_operation='merge')
                kw['response'] = "edited"
            else:
                raise KeyError("no operation (get, get_config, edit_config) specified")
            kw['language'] = 'xml'

    else:
        kw['xml'] = default_xml

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
