import json
from collections import Counter

'''
with open('index_clase.json') as js:
    index = json.load(js)
with open('todos_asan.json') as js:
    asan = json.load(js)

# Diccionario de problema/equipo a lista de envíos
agrupado = {}

# Agrupa los diagnósticos por problema/equipo
for sid, data in index.items():
    # No nos interesan los CE
    if data['result'] == 'CE':
        continue

    problema = agrupado.setdefault(data['problem'], {})
    equipo = problema.setdefault(data['team'], [])

    try:
        submission = asan[sid]
        has_asan = True
    except KeyError:
        has_asan = False

    if has_asan:
        for key, value in submission.items():
            if key == 'team' or key == 'judge_result':
                continue

            data['runs'][int(key) - 1]['asan_error'] = value

    equipo.append({'runs': data['runs'], 'sid': sid, 'result': data['result'], 'has_asan': has_asan})

with open('agrupados_asan.json', 'w') as js:
    json.dump(agrupado, js, indent=2)
'''


with open('agrupados_asan.json') as js:
    agrupado = json.load(js)

# Veces que la eliminación de un diagnóstico está relacionado con un paso a AC
inACtrans = Counter()
envios = Counter()

# Estudia transiciones de veredicto y su relación con los diagnósticos
for problem in agrupado.values():
    found_problem = set()

    for team in problem.values():
        found_pair = set()

        for k, submission in enumerate(team):
            if k > 0 and team[k - 1]['result'] != 'AC' and team[k - 1]['has_asan']:
                for j, run in enumerate(submission['runs']):
                    try:
                        if run['result'] == 'AC' and run.get('asan_error', 'noerror') == 'noerror' \
                                and team[k - 1]['runs'][j].get('asan_error', 'noerror') != 'noerror' \
                                and team[k - 1]['runs'][j]['result'] != 'AC':
                            error = team[k - 1]['runs'][j]['asan_error']
                            inACtrans[error] += 1
                            envios[(submission['sid'], team[k - 1]['sid'])] += 1
                    except KeyError:
                        pass

od = dict(sorted(inACtrans.items(), key=lambda item: item[1], reverse=True))

for key, value in od.items():
    print(key + ': ' + str(value))

print(len(envios))
