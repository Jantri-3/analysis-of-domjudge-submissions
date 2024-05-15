import json
import os
import xml.etree.ElementTree as ET


def parse_xml_inputs(folder, output, out_type):
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
                if not isRelevantErrorCPP(error.attrib['id']):
                    continue
                else:
                    error_object = {'level': error.attrib['severity'], 'message': error.attrib['msg'],'error_name': error.attrib['id']}
                    list_errors.append(error_object)

            json_object[id_envio]['error_list'] = list_errors

        output_file.write(json.dumps(json_object))

    index.close()


def count_errorsCPP(filename):
    file = open(filename)
    counter = 0
    file_json = json.load(file)
    countserror = dict()
    for envio in file_json:
        try:
            for error in file_json[envio]['error_list']:
                #countserror[error['level']] = countserror.get(error['level'], 0) + 1
                if error['level']  == "note":
                    countserror[error['error_name']] = countserror.get(error['error_name'], 0) + 1
                    counter = counter + 1 
                else:
                    continue
        except KeyError:
            continue
    for key, value in sorted(countserror.items(), key=lambda x: x[1], reverse=True):
        print(key + ': ' + str(value))
    print (len(countserror.items()))


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

errores_relevantes_cppcheck = ['uninitvar',
                               'unreadVariable',
                               'shadowFunction',
                               'shadowVariable',
                               'shadowArgument',
                               'knownConditionTrueFalse',
                               'redundantCondition',
                               'multiCondition',
                               'duplicateExpression',
                               'duplicateBreak',
                               'uninitStructMember',
                               'syntaxError',
                               'noConstructor',
                               'unreachableCode',
                               'knownEmptyContainer',
                               'clarifyCondition',
                               'selfAssignment',
                               'negativeContainerIndex',
                               'containerOutOfBounds',
                               'identicalInnerCondition',
                               'passedByValue',
                               'stlFindInsert',
                               'iterateByValue',
                               'useInitializationList',
                               'missingReturn',
                               'legacyUninitvar',
                               'internalAstError',
                               'selfInitialization',
                               'constStatement']

def isRelevantErrorCPP(error_name: str):
    if error_name in errores_relevantes_cppcheck:
        return True

if __name__ == '__main__':
    parse_xml_inputs('./cppchecktodos', 'claseCppcheck.json', 'Cppcheck')
    count_errorsCPP('claseGcc.json')