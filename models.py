import pyang
import itertools

def load(path, models):
    repos = pyang.FileRepository(path)
    ctx = pyang.Context(repos)
    modules = []
    for fname in models:
        fd = open(fname, 'r')
        text = fd.read()
        module = ctx.add_module(fname, text)
        if module:
            modules.append(module)
    return modules, ctx
        

def create_jstreedata(modules, ctx):
    nodelist = []
    nodeid = itertools.count(1)
    for m in modules:
        def add_child(stmt):
            node = { 'id': nodeid.next(), 'text': "{}:{}".format(stmt.i_module.i_prefix, stmt.arg) }
            if hasattr(stmt, "i_children"):
                children = []
                for child in stmt.i_children:
                    children.append(add_child(child))
                node['children'] = children
            return node
        modulenode = { 'id': nodeid.next(), 'text': m.arg }
        modulechildren = []
        for stmt in m.i_children:
            modulechildren.append(add_child(stmt))
        if len(modulechildren) > 0:
            modulenode['children'] = modulechildren
            nodelist.append(modulenode)
    if len(nodelist) > 0:
        return { 'core': { 'data': nodelist } }
    else:
        return None
