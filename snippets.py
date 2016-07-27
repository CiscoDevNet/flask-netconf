#
# Some list of snippets, one for each of get, get-config & edit-config
#
get = [
    '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>''',
    '''<interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>''',
    '''<routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>''',
    '''<bgp-state xmlns="urn:cisco:params:xml:ns:yang:cisco-bgp-state"/>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios"/>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip/>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip><access-list/></ip>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip><route/></ip>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <router>
    <bgp/>
  </router>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <router>
    <ospf/>
  </router>
</native>''',
]


get_config = [
]


edit_config = [
]
