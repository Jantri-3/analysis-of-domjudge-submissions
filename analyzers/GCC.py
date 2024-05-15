import json
import os


def parse_GCC_outputs(folder, output, out_type):
    index = open(os.path.join(folder, 'index_clase.json'))
    index_json = json.load(index)
    with open(os.path.join('.', output), 'w', newline='') as output_file:
        # directory, resultado_judge, resultado_clang, len_lista, mensajes
        json_object = {}

        for directory, subdirectory, files in os.walk(folder):
            if directory == folder:  # skips root
                continue

            id_envio = directory.replace(folder + "/", '')
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
                    if not isRelevantErrorGCC(result['ruleId']):
                        continue
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



def count_error_names(filename):
    file = open(filename)
    file_json = json.load(file)
    counts = dict()
    for envio in file_json:
        try:
            for error in file_json[envio]['error_list']:
                counts[error['error_name']] = counts.get(error['error_name'], 0) + 1
        except KeyError:
            continue
    for key, value in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(key + ': ' + str(value))

errores_relevantes_GCC = [
'error',
'fatal error',
'warning',
'-fpermissive',
'-Wchanges-meaning',
'-Wvexing-parse']

def isRelevantErrorGCC(error_name: str):
    if error_name in errores_relevantes_GCC:
        return True


if __name__ == '__main__':
    parse_GCC_outputs('./gcctodos', 'claseGcc.json', 'GCC')
    #count_error_names('claseGcc.json')
