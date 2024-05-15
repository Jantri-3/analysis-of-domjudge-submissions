import csv
import json
import os
import statistics
from collections import Counter

import yaml

'''# Carga el índice de la clase
with open('index_clase.json') as js:
	index = json.load(js)

# Diccionario de problema/equipo a lista de envíos
agrupado = {}

# Agrupa los diagnósticos por problema/equipo
for sid, data in index.items():
	# No nos interesan los CE
	if data['result'] == 'CE':
		continue

	problema = agrupado.setdefault(data['problem'], {})
	equipo = problema.setdefault(data['team'], [])
	found = set()

	if os.path.exists(f'{sid}/Tidy.yaml'):
		# Carga el resultado de clang-tidy
		with open(f'{sid}/Tidy.yaml') as td:
			info = yaml.safe_load(td)

		for diag in info['Diagnostics']:
			found.add(diag['DiagnosticName'])

	equipo.append({'runs': data['runs'], 'sid': sid, 'result': data['result'], 'diags': list(found)})

with open('agrupados.json', 'w') as js:
	json.dump(agrupado, js, indent=2)'''

with open('agrupados.json') as js:
	agrupado = json.load(js)

# Cuenta envíos de cada subproblema con distintos criterios
byproblem = Counter()
bypair = Counter()
bysubm = Counter()

for problem in agrupado.values():
	found_problem = set()

	for team in problem.values():
		found_pair = set()

		for submission in team:
			for diag in submission['diags']:
				bysubm[diag] += 1
				if diag not in found_pair:
					found_pair.add(diag)
					bypair[diag] += 1

					if diag not in found_problem:
						found_problem.add(diag)
						byproblem[diag] += 1


# Veces que la eliminación de un diagnóstico está relacionado con un paso a AC
inACtrans = Counter()

# Estudia transiciones de veredicto y su relación con los diagnósticos
for problem in agrupado.values():
	found_problem = set()

	for team in problem.values():
		found_pair = set()

		for k, submission in enumerate(team):
			if k > 0 and team[k - 1]['result'] != 'AC' and submission['result'] == 'AC':
				removed = set(team[k - 1]['diags']) - set(submission['diags'])

				if not removed:
					inACtrans['empty'] += 1
				else:
					for name in removed:
						inACtrans[name] += 1
				break
			else:
				prev = submission['result']


with open('cuentas.csv', 'w') as csvf:
	csvw = csv.writer(csvf)
	csvw.writerow(('diagnostic', 'byproblem', 'bypair', 'bysubm', 'inACtrans'))

	for name, count_problem in byproblem.items():
		count_pair = bypair[name]
		count_subm = bysubm[name]
		count_ac = inACtrans.get(name, 0)

		csvw.writerow((name, count_problem, count_pair, count_subm, count_ac))

	csvw.writerow(('empty', 0, 0, 0, inACtrans.get('empty', 0)))
