from graphs import graph_f, graph_s

inv_f = {}
for k, v in graph_f.items():
	for vv in v:
		inv_f[vv] = inv_f.get(vv, []) + [k]

inv_s = {}
for k, v in graph_s.items():
	for vv in v:
		inv_s[vv] = inv_s.get(vv, []) + [k]

start_nodes_f = [k for k in graph_f if k not in inv_f]
print("Start nodes of graph_f:", start_nodes_f)
start_nodes_s = [k for k in graph_s if k not in inv_s]
print("Start nodes of graph_s:", start_nodes_s)

def find_path(graph, start_node):
	path = []
	stack = [start_node]
	while stack:
		node = stack.pop()
		path.append(node)
		if node in graph:
			stack.extend(graph[node])
	return path

for s in start_nodes_f:
	path_f = find_path(graph_f, s)
	print(len(path_f), path_f)
