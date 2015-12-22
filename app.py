# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from jinja2 import Template
from ncclient import manager
from ncclient.operations import RPCError
from ncclient.transport import SSHError

# create the application object
app = Flask(__name__)

#
# The Template Python Script for get requests
#
script_template=Template("""
#!/usr/bin/env python
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
    return redirect(url_for('netconf'))

@app.route('/netconf', methods=['GET', 'POST'])
def netconf():
    kw = {}
    if request.method=='POST':
        # TODO: hacky dict copy
        for k,v in request.form.iteritems():
            kw[k] = v
        if kw['submit']=='generate':
            kw['response'] = script_template.render(FILL_THIS=kw['xml'])
        elif kw['submit']=='send':
            try:
                m =  manager.connect(host=kw['device_ip'],
                                     port=int(kw['device_port']),
                                     username=kw['username'],
                                     password=kw['password'],
                                     device_params={'name':"csr"})
                kw['response'] = m.get('<filter>'+kw['xml']+'</filter>')
                m.close_session()
            except RPCError as e:
                kw['response'] = e.info
            except SSHError as e:
                kw['response'] = e.message
            except:
                kw['response'] = 'Unknown error!!'
    else:
        kw['xml'] = default_xml
    return render_template('code-generator.html', **kw)  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0". port=8080)
    netconf
