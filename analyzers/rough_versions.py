import json
import yaml
import os
import xml.etree.ElementTree as ET

'''
First version of separate parsers for analysis and analysis code
It's a rough version that was polished later
'''


def parse_clang_outputs(folder, output, out_type):
    index = open(os.path.join(folder, 'index.json'))
    index_json = json.load(index)
    with open(os.path.join('.', output), 'w', newline='') as output_file:
        # directory, resultado_judge, resultado_clang, len_lista, mensajes
        json_object = {}

        for directory, subdirectory, files in os.walk(folder):
            if directory == folder:  # skips root
                continue

            id_envio = directory.replace(folder + '\\', '')
            json_object[id_envio] = {}
            json_object[id_envio]['judge_result'] = index_json[id_envio]['result']

            input_file = [x for x in files if x.startswith(out_type)]
            if len(input_file) == 0:
                json_object[id_envio]['lasan_result'] = 'no input file'
                continue

            input_file = input_file[0]
            with open(os.path.join(directory, input_file)) as json_output:
                results = json.load(json_output)['runs'][0]['results']
                len_results = len(results)

                if len_results == 0:
                    json_object[id_envio]['lasan_result'] = 'no errors'
                    continue

                json_object[id_envio]['lasan_result'] = 'has errors'
                json_object[id_envio]['num_errors'] = len_results

                list_errors = []
                for result in results:
                    try:
                        error_object = {'level': result['level'], 'message': result['message']['text'],
                                        'error_name': result['ruleId']}
                    except KeyError:
                        error_object = {'level': 'Header not found', 'message': result['message']['text'],
                                        'error_name': result['ruleId']}
                    list_errors.append(error_object)

                json_object[id_envio]['error_list'] = list_errors

        output_file.write(json.dumps(json_object))

    index.close()


def parse_xml_inputs(folder, output, out_type):
    index = open(os.path.join(folder, 'index.json'))
    index_json = json.load(index)
    with open(os.path.join('.', output), 'w', newline='') as output_file:
        # directory, resultado_judge, resultado_clang, len_lista, mensajes
        json_object = {}

        for directory, subdirectory, files in os.walk(folder):
            if directory == folder:  # skips root
                continue

            id_envio = directory.replace(folder + '\\', '')
            json_object[id_envio] = {}
            json_object[id_envio]['judge_result'] = index_json[id_envio]['result']

            input_file = [x for x in files if x.startswith(out_type)]
            if len(input_file) == 0:
                json_object[id_envio]['lasan_result'] = 'no input file'
                continue

            input_file = input_file[0]
            tree = ET.parse(os.path.join(directory, input_file))
            root = tree.getroot()

            len_results = len(root[1])

            if len_results == 0:
                json_object[id_envio]['lasan_result'] = 'no errors'
                continue

            json_object[id_envio]['lasan_result'] = 'has errors'
            json_object[id_envio]['num_errors'] = len_results

            list_errors = []
            for error in root[1]:
                error_object = {'level': error.attrib['severity'], 'message': error.attrib['msg']}
                list_errors.append(error_object)

            json_object[id_envio]['error_list'] = list_errors

        output_file.write(json.dumps(json_object))

    index.close()


def parse_yaml_inputs(folder, output, out_type):
    index = open('index_clase.json')
    index_json = json.load(index)
    with open(os.path.join('.', output), 'w', newline='') as output_file:
        # directory, resultado_judge, resultado_clang, len_lista, mensajes
        json_object = {}

        for directory, subdirectory, files in os.walk(folder):
            if directory == folder:  # skips root
                continue

            id_envio = directory.replace(folder + '\\', '')
            json_object[id_envio] = {}
            json_object[id_envio]['judge_result'] = index_json[id_envio]['result']
            json_object[id_envio]['team'] = index_json[id_envio]['team']

            input_file = [x for x in files if x.startswith(out_type)]
            if len(input_file) == 0:
                json_object[id_envio]['lasan_result'] = 'no input file'
                continue

            input_file = input_file[0]
            input_file = open(os.path.join(directory, input_file))
            yaml_input = yaml.safe_load(input_file)
            len_results = len(yaml_input['Diagnostics'])

            if len_results == 0:
                json_object[id_envio]['lasan_result'] = 'no errors'
                continue

            json_object[id_envio]['lasan_result'] = 'has errors'
            json_object[id_envio]['num_errors'] = len_results

            list_errors = []
            for error in yaml_input['Diagnostics']:
                if not isRelevantError(error['DiagnosticName']):
                    continue
                error_object = {'level': error['Level'], 'message': error['DiagnosticMessage']['Message'],
                                'error_name': error['DiagnosticName'], 'file': error['DiagnosticMessage']['FilePath']}
                list_errors.append(error_object)

            json_object[id_envio]['error_list'] = list_errors

            input_file.close()

        output_file.write(json.dumps(json_object))

    index.close()


def parseLogs(folder: str, filename: str, outFile: str):
    json_object = {}
    index = open('index_clase.json')
    index_json = json.load(index)
    for directory, subdirectory, files in os.walk(folder):
        if directory == folder or len(subdirectory) == 0:  # skips root
            continue
        id_envio = directory.replace('asan_todos\\', '')
        json_object[id_envio] = {}

        hasFiles = False

        for case in subdirectory:
            for fi in os.listdir(os.path.join(directory, case)):
                if fi != filename:
                    continue

                hasFiles = True

                with open(os.path.join(directory, case, fi), 'r') as readFile:
                    if filename == 'lasan.log':
                        second_line = readFile.readlines()[1]
                        index = 34
                        if second_line[16] == 'L':
                            index = 31
                        error = second_line[index:]
                        index = error.find(' on')
                        json_object[id_envio][case] = error[:index] # + ';' + index_json[id_envio]['runs'][int(case) - 1]['result']
                    else:
                        line = readFile.readlines()[0]
                        error = line.split(':')[4]
                        json_object[id_envio][case] = error[1:14] + ';' + index_json[id_envio]['runs'][int(case) - 1]['result']

        if hasFiles:
            json_object[id_envio]['judge_result'] = index_json[id_envio]['result']
            json_object[id_envio]['team'] = index_json[id_envio]['team']

    json_object = {k: v for k, v in json_object.items() if bool(v)}

    with open(os.path.join('.', outFile), 'w', newline='') as output_file:
        output_file.write(json.dumps(json_object))


def count_error_names(filename):
    file = open(filename)
    file_json = json.load(file)
    counts = dict()
    for envio in file_json:
        print(envio)
        try:
            for error in file_json[envio]['error_list']:
                counts[error['error_name']] = counts.get(error['error_name'], 0) + 1
        except KeyError:
            continue
    for key, value in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(key + ': ' + str(value))


def counter(filename):
    file = open(filename)
    file_json = json.load(file)
    count = 0
    lista = []
    for envio in file_json:
        try:
            for error in file_json[envio]['error_list']:
                if error['error_name'] == 'performance-for-range-copy':
                    print(envio)
                    count += 1
            if count != 0:
                lista.append((count, file_json[envio]['judge_result'], envio))
                count = 0
        except KeyError:
            continue
    print(lista)


def isIrrelevantError(errorName: str):
    irrelevant_error_names = ['llvm', 'altera', 'google', 'concurrency', 'readability', 'fuchsia', 'modernize', 'cert']

    for name in irrelevant_error_names:
        if errorName.startswith(name):
            return True


relevant_errors = ['bugprone-narrowing-conversions',
                   'bugprone-exception-escape',
                   'clang-analyzer-cplusplus.NewDelete',
                   'clang-analyzer-deadcode.DeadStores',
                   'bugprone-suspicious-semicolon',
                   'bugprone-integer-division',
                   'bugprone-branch-clone',
                   'misc-redundant-expression',
                   'performance-for-range-copy',
                   'performance-unnecessary-value-param',
                   'bugprone-infinite-loop']


def isRelevantError(error_name: str):
    if error_name in relevant_errors:
        return True


def countAllResults():
    index = open('index_clase.json')
    index_json = json.load(index)
    dic = {'WA': 0, 'CE': 0, 'RTE': 0, 'TLE': 0, 'AC': 0, 'NO': 0, 'OLE': 0}
    count = 0
    for id_envio in index_json:
        dic[index_json[id_envio]['result']] += 1
        count += 1
    print('count: ' + str(count))
    print(dic)
    s = sum(dic.values())
    dic = {key: str(round((dic[key] * 100.0 / s), 2)) + "%" for key in dic.keys()}
    print(dic)


def countErrorByGroup(filename: str):
    error_indexes = {val: idx for idx, val in enumerate(relevant_errors)}
    list_dicts_results = [dict() for _ in relevant_errors]

    file = open(filename)
    file_json = json.load(file)

    index = open('index_clase.json')
    index_json = json.load(index)

    for id_envio in file_json:
        if index_json[id_envio]['problem'] != '261':
            continue
        team = file_json[id_envio]['team']
        try:
            for error in file_json[id_envio]['error_list']:
                error_index = error_indexes[error['error_name']]
                list_dicts_results[error_index][team] = list_dicts_results[error_index].get(team, 0) + 1

        except KeyError:
            continue

    for error, dic in zip(relevant_errors, list_dicts_results):
        od = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
        print(error, ': ', od)


def prueba():
    lasan_errors = [
        'stack-use-after-return',
        'SEGV',
        'heap-buffer-overflow',
        'stack-overflow',
        'detected memory leaks',
        'heap-use-after-free',
        'global-buffer-overflow'
    ]
    error_indexes = {val: idx for idx, val in enumerate(lasan_errors)}
    list_num_errors = [0, 0, 0, 0, 0, 0, 0]
    index = open('todos_ubsan.json')
    index_json = json.load(index)
    for envio in index_json.values():
        index = error_indexes[list(envio.values())[0]]
        list_num_errors[index] += 1

    for error, num in zip(lasan_errors, list_num_errors):
        print(error, ': ', num)


def prueba2():
    index = open('todos_ubsan.json')
    index_json = json.load(index)

    results = dict()
    count = 0

    for envio in index_json.values():
        for k, v in envio.items():
            if k == 'judge_result' or k == 'team':
                continue
            count += 1
            results[v] = results.get(v, 0) + 1

    print(results)
    od = dict(sorted(results.items(), key=lambda item: item, reverse=True))
    print( od)

    sums = 0
    for k, v in od.items():
        print(k + ': ' + str(v))
        sums += v
    print(sums)


def prueba3():
    index = open('todos_asan.json')
    index_json = json.load(index)

    results = dict()
    count = 0

    for envio in index_json.values():
        count += 1
    print(count)


def contarEquipos():
    lasan_errors = [
        'stack-use-after-return',
        'SEGV',
        'heap-buffer-overflow',
        'stack-overflow',
        'detected memory leaks',
        'heap-use-after-free',
        'global-buffer-overflow'
    ]

    error_indexes = {val: idx for idx, val in enumerate(lasan_errors)}
    list_dicts_results = [dict() for _ in lasan_errors]
    dict_teams = dict()

    index = open('todos_asan.json')
    index_json = json.load(index)

    for envio in index_json:
        dict_teams[index_json[envio]['team']] = dict_teams.get(index_json[envio]['team'], 0) + 1

    od = dict(sorted(dict_teams.items(), key=lambda item: item[1], reverse=True))
    print(od)


def contarUbsan():
    index = open('todos_ubsan_sin_judge_per_case.json')
    index_json = json.load(index)

    results = dict()

    for envio in index_json.values():
        for k, v in envio.items():
            if k == 'judge_result' or k == 'team':
                continue
            results[v] = results.get(v, 0) + 1

    od = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    print(od)


def parseLogs2(folder: str, filename: str, outFile: str):
    json_object = {}
    count = 0

    for directory, subdirectory, files in os.walk(folder):
        if directory == folder or len(subdirectory) == 0:  # skips root
            continue
        id_envio = directory.replace('asan_todos\\', '')
        json_object[id_envio] = {}

        hasFiles = False

        for case in subdirectory:
            for fi in os.listdir(os.path.join(directory, case)):
                if fi != filename:
                    continue

                hasFiles = True

                with open(os.path.join(directory, case, fi), 'r') as readFile:
                    lines = readFile.readlines()
                    if len(lines) > 1:
                        notRepeated = True
                        listErrors = []
                        i = 0
                        while notRepeated and i < len(lines):
                            error = lines[i].split(':')[4][1:14]
                            if error not in listErrors and len(listErrors) > 0:
                                notRepeated = False
                            else:
                                listErrors.append(error)
                                i += 1
                        if notRepeated:
                            print('idEnvio: ' + id_envio)
                            print('case: ' + case)
                            print(lines)
                            print('='*60)
                            count += 1
    print(count)


if __name__ == '__main__':
    # parse_clang_outputs('./estático_clase', 'claseClang.json', 'Clang')
    # parse_clang_outputs('./estático_clase', 'claseGcc.json', 'GCC')
    # parse_xml_inputs('./estático_clase', 'claseCppcheck.json', 'Cppcheck')
    # parse_xml_inputs('./estático_clase', 'claseCppcheckexhaust.json', 'CppcheckExhaust')
    # parse_yaml_inputs('./todos_clase_clang_tidy', 'claseTidyTodosSoloRelevantes.json', 'Tidy')
    count_error_names('claseTidyTodos.json')
    # counter('claseTidyTodos.json')
    # countAllResults()
    # parseLogs('asan_todos', 'ubsan.log', 'todos_ubsan.json')
    # parseLogs('asan_todos', 'asan.log', 'todos_asan_sin_judge_per_case.json')
    # countErrorByGroup('claseTidyTodosSoloRelevantes.json')
    # prueba2()
    # contarEquipos()
    # contarUbsan()
    # parseLogs2('asan_todos', 'ubsan.log', 'todos_ubsan.json')