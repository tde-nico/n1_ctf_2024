import idautils
import idaapi
import idc


DEBUG = 0
RENAME = 1
GRAPH = 0

graph_f = {}
graph_s = {}


def retrive(func):
	fun = idaapi.get_func(func)
	size = fun.size()
	start = fun.start_ea
	blocks = []
	first = None
	second = None
	switch = False
	if DEBUG:
		print(f'func -> {idc.get_func_name(func)}')


	while start < func + size:
		addr = start
		inst = idc.generate_disasm_line(addr, 0)
		
		if 'blocks' in inst:
			tmp = inst.split('blocks')[1].split(', ')[0]
			tmp = tmp.replace('+', '').replace('h', '')
			if tmp == '':
				tmp = 0
			else:
				tmp = int(tmp, 16) // 8
			if DEBUG:
				print(tmp)
			blocks.append(tmp)
		
		elif 'blockz' in inst:
			tmp = inst.split('blockz')[1].split(', ')[0]
			tmp = tmp.replace('+', '').replace('h', '')
			if tmp == '':
				tmp = 0
			else:
				tmp = int(tmp, 16) // 8
			if DEBUG:
				print(tmp)
			blocks.append(tmp)
			switch = True

		elif 'first_' in inst:
			first = inst.split('first_')[1].split(', ')[0]
		
		elif 'second_' in inst:
			second = inst.split('second_')[1].split(', ')[0]

		start = idc.next_head(start)


	if blocks:
		# if len(blocks) == 2:
		# 	if not switch:
		# 		print(f'{blocks[0]}-{blocks[1]}')

		if GRAPH:
			if not switch:
				if first:
					tmp = f'end_{first}'
				elif second:
					tmp = f'end_{second}'
				else:
					tmp = blocks[1]
				graph_f[blocks[0]] = graph_f.get(blocks[0], []) + [tmp]
			else:
				if first:
					tmp = f'end_{first}'
				elif second:
					tmp = f'end_{second}'
				else:
					tmp = blocks[1]
				graph_s[blocks[0]] = graph_s.get(blocks[0], []) + [tmp]
		
		if RENAME:
			if not switch:
				name = f"f_{blocks[0]}_"
			else:
				name = f"s_{blocks[0]}_"
			if len(blocks) == 2:
				name += f"{blocks[1]}"
				idaapi.set_name(func, name, idaapi.SN_CHECK)
			elif len(blocks) == 1:
				if first:
					name += f"first_{first}"
				else:
					name += f"second_{second}"
				idaapi.set_name(func, name, idaapi.SN_CHECK)



for func in idautils.Functions():
	retrive(func)

if GRAPH:
	print('Graph F')
	print(graph_f)
	print('Graph S')
	print(graph_s)


print('Done')

