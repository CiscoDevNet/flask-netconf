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
    '''<native xmlns="urn:ios"/>''',
    '''<native xmlns="urn:ios">
  <ip/>
</native>''',
    '''<native xmlns="urn:ios">
  <ip><access-list/></ip>
</native>''',
    '''<native xmlns="urn:ios">
  <ip><route/></ip>
</native>''',
    '''<native xmlns="urn:ios">
  <router>
    <bgp/>
  </router>
</native>''',
    '''<native xmlns="urn:ios">
  <router>
    <ospf/>
  </router>
</native>''',
]


get_config = [
]


edit_config = [
]
