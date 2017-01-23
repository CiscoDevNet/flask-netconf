from jinja2 import Template

get_script_template=Template("""#!/usr/bin/env python
data = '''
  {{FILL_THIS}}
'''

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

    m = manager.connect(host=args.host,
                        port=args.port,
                        username=args.username,
                        password=args.password,
                        device_params={'name': "csr"})
    {{ACTION}}
""")

action = {
    "get" : "print m.get('<filter>' + data + '</filter>').data_xml\n\tprint",
    "get_config" : "print m.get_config(source='running', filter=('subtree', data)).data_xml",
    "edit_config" : "m.edit_config(data, target='running', format='xml',default_operation='merge')"
}