import json
from collections import Counter


def countResultsPerDiagnostic():
    with open('agrupados.json') as js:
        agrupado = json.load(js)

    diag_and_result = Counter()

    for problem in agrupado.values():
        for team in problem.values():
            for submission in team:
                for diag in submission['diags']:
                    diag_and_result[(diag, submission['result'])] += 1

    od = dict(sorted(diag_and_result.items(), key=lambda item: item[0]))

    list_errors = []
    list_dicts = []
    count = -1

    for key, value in od.items():
        if key[0] not in list_errors:
            list_errors.append(key[0])
            list_dicts.append({key[1]: value})
            count += 1
        else:
            list_dicts[count][key[1]] = value

    with open('count_results.txt', 'w') as file:
        for i in range(len(list_errors)):
            file.write(list_errors[i] + ': ' + str(list_dicts[i]) + '\n')

    with open('count_results_percent.txt', 'w') as file:
        for i in range(len(list_errors)):
            s = sum(list_dicts[i].values())
            list_dicts[i] = \
                {key: str(round((list_dicts[i][key] * 100.0 / s), 2)) + "%" for key in list_dicts[i].keys()}
            file.write(list_errors[i] + ': ' + str(list_dicts[i]) + '\n')


if __name__ == '__main__':
    countResultsPerDiagnostic()
