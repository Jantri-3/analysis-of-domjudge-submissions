import csv
import json
from collections import Counter

with open('agrupados_asan.json') as js:
    agrupado = json.load(js)

# Cuenta envíos de cada subproblema con distintos criterios
byproblem = Counter()
bypair = Counter()
bysubm = Counter()
bytestcase = Counter()
byresult = Counter()
byresultwithouterror = Counter()
bysubmwithouterror = Counter()

for problem in agrupado.values():
    found_problem = set()
    empty_problem = True

    for team in problem.values():
        found_pair = set()
        empty_pair = True

        for submission in team:
            found_sub = set()

            if submission['has_asan']:
                bysubmwithouterror[submission['result']] += 1
                empty_problem = False
                empty_pair = False
                for run in submission['runs']:
                    try:
                        error = run['asan_error']
                        result = run['result']
                        byresultwithouterror[result] += 1
                        byresult[(error, result)] += 1
                        bytestcase[error] += 1
                        if error not in found_sub:
                            found_sub.add(error)
                            bysubm[error] += 1
                            if error not in found_pair:
                                found_pair.add(error)
                                bypair[error] += 1
                                if error not in found_problem:
                                    found_problem.add(error)
                                    byproblem[error] += 1

                    except KeyError:
                        pass

            else:  # poner empty +1
                bytestcase['empty'] += 1
                bysubm['empty'] += 1
                if empty_pair:
                    bypair['empty'] += 1
                if empty_problem:
                    byproblem['empty'] += 1

with open('cuentas_asan.csv', 'w') as csvf:
    csvw = csv.writer(csvf)
    csvw.writerow(('diagnostic', 'byproblem', 'bypair', 'bysubm', 'bytestcase'))

    for name, count_problem in byproblem.items():
        count_pair = bypair[name]
        count_subm = bysubm[name]
        count_bytestcase = bytestcase[name]

        csvw.writerow((name, count_problem, count_pair, count_subm, count_bytestcase))

    od = dict(sorted(byresult.items(), key=lambda item: item[0]))

    lista_errors = []
    lista_dicts = []
    count = -1

    for key, value in od.items():
        if key[0] not in lista_errors:
            lista_errors.append(key[0])
            lista_dicts.append({key[1]: value})
            count += 1
        else:
            lista_dicts[count][key[1]] = value

    with open('count_results_asan.txt', 'w') as file:

        for i in range(len(lista_errors)):
            file.write(lista_errors[i] + ': ' + str(lista_dicts[i]) + '\n')
        file.write('bytestcase by test: ' + str(byresultwithouterror))
        s = sum(byresultwithouterror.values())
        byresultwithouterror = \
            {key: str(round((byresultwithouterror[key] * 100.0 / s), 2)) + "%" for key in byresultwithouterror.keys()}
        file.write('bytestcase by sub: ' + str(bysubmwithouterror))

        s = sum(bysubmwithouterror.values())
        bysubmwithouterror = \
            {key: str(round((bysubmwithouterror[key] * 100.0 / s), 2)) + "%" for key in bysubmwithouterror.keys()}

    with open('count_results_asan_percent.txt', 'w') as file:
        for i in range(len(lista_errors)):
            s = sum(lista_dicts[i].values())
            lista_dicts[i] = \
                {key: str(round((lista_dicts[i][key] * 100.0 / s), 2)) + "%" for key in lista_dicts[i].keys()}
            file.write(lista_errors[i] + ': ' + str(lista_dicts[i]) + '\n')

        file.write('bytestcase by test: ' + str(byresultwithouterror))
        file.write('bytestcase by sub: ' + str(bysubmwithouterror))
