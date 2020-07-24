import io

def get_transitive_edges(nodes):

    def dfs(g, node, visited, path, paths):
        visited.add(node)
        path.append(node)
        if not g[node]:
            paths.append(list(path))
        elif node in g:
            for i in g[node]:
                if i not in visited:
                    _ = dfs(g, i, visited, path, paths)
        path.pop()
        visited.remove(node)
        return paths

    def all_paths(g, origin):
        visited = set()
        path = []
        paths = []
        _ = dfs(g, origin, visited, path, paths)
        return paths

    ret = set()
    for node_id in nodes:
        result = set(
            [
                (node_id, node_parent) for transitive_edge in [
                    set(path_to_node[2:]).intersection(nodes[node_id]) for path_to_node in all_paths(nodes, node_id)
                ] for node_parent in transitive_edge
            ]
        )
        if result:
            ret = ret.union(result)
    return ret

def process_list(graph):
    nodes = {}
    for (child_id, parent_id) in graph:
        if child_id not in nodes:
            nodes[child_id] = set()
        nodes[child_id].add(parent_id)
        if not parent_id in nodes:
            nodes[parent_id] = set()
    ret = get_transitive_edges(nodes)
    return ret

def process_dict(graph):
    nodes = {}
    for child_id in graph:
        if child_id not in nodes:
            nodes[child_id] = set()
        for parent_id in graph[child_id]:
            nodes[child_id].add(parent_id)
            if not parent_id in nodes:
                nodes[parent_id] = set()
    ret = get_transitive_edges(nodes)
    return ret

def process_tabfile(graph):
    nodes = {}
    for line in graph:
        child_id, parent_id = line.strip('\n').split('\t')[:2]
        if child_id not in nodes:
            nodes[child_id] = set()
        nodes[child_id].add(parent_id)
        if parent_id not in nodes:
            nodes[parent_id] = set()
    ret = get_transitive_edges(nodes)
    return ret

def transitive_edges(graph):
    def iterable(obj):
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True
    if not iterable(graph):
        raise ValueError
    if isinstance(graph, list) or isinstance(graph, tuple):
        return process_list(graph)
    elif isinstance(graph, dict):
        return process_dict(graph)
    elif isinstance(graph, io.TextIOWrapper):
        return process_tabfile(graph)
    else:
        raise ValueError
