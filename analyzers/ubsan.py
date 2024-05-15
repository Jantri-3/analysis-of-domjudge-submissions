import json
import os
import re


def parseLogs(folder: str, filename: str, outFile: str): 
    json_object = {}
    count = 0
    with open('index_clase.json', 'r') as index:
        index_json = json.load(index)

    for directory, subdirectory, files in os.walk(folder):
        if directory == folder or len(subdirectory) == 0:  # skips root
            continue
        id_envio = directory.replace('asan_todos/', '')
        json_object[id_envio] = {}

        hasFiles = False

        
        #general list of cases
        generalist = set()
        for case in subdirectory:
        
            
            for fi in os.listdir(os.path.join(directory, case)):
                if fi != filename:
                    continue

                hasFiles = True
                

                with open(os.path.join(directory, case, fi), 'r') as readFile:
                    list_errors = set()
                    lines = readFile.readlines()
                    for line in lines:
                        if line == '\n':
                            continue

                        try:
                            error = line.split(':')[4]#[1:14]
                            error = re.sub( "\d" , '',error)
                            error = re.sub( r"of type.*" , '',error)
                            pattern = r"(overflowed)( to (xa|xb|xc|xd|xe|xf).*)?$"
                            error = re.sub( pattern, r"\1",error)
                            pattern2 = r"(base)( (x|xa|xb|xc|xd|xe|xf).*)?$"
                            error = re.sub( pattern2, r"\1",error)
                            pattern3 = r"(address)( (x|xa|xb|xc|xd|xe|xf).*)?$"
                            error = re.sub( pattern3, r"\1",error)
                            error = re.sub("\n", "", error)


                        except IndexError:
                            continue

                        #if error repited a general list of cases = NOT APPEND
                       
                        if error not in generalist:
                            generalist.add(error)
                            list_errors.add(error)
                       

                    json_object[id_envio][case] = {}
                    json_object[id_envio][case]['list_errors'] = list(list_errors)
                    json_object[id_envio][case]['judge_result'] = index_json[id_envio]['runs'][int(case) - 1]['result']
                    count += 1

        if hasFiles:
            json_object[id_envio]['judge_result'] = index_json[id_envio]['result']
            json_object[id_envio]['team'] = index_json[id_envio]['team']


    json_object = {k: v for k, v in json_object.items() if bool(v)}

    with open(os.path.join('.', outFile), 'w', newline='') as output_file:
        output_file.write(json.dumps(json_object,indent=2))


def listaErrores():
    with open('index_clase.json', 'r') as index:
        index_json = json.load(index)


def count_errorsUbsan(filename):
    file = open(filename)
    counter = 0
    file_json = json.load(file)
    countserror = dict()
    for envio in file_json:
        try:
            for case in file_json[envio]:
                try:
                    isinstance(int(case), int)
                    for error in file_json[envio][case]['list_errors']:
                        countserror[error] = countserror.get(error, 0) + 1
                        counter = counter + 1 
                except ValueError:
                    continue
        except KeyError:
            continue
    for key, value in sorted(countserror.items(), key=lambda x: x[1], reverse=True):
        print(key + ': ' + str(value))
    print (len(countserror.items()))

def count_result(filename):
    errors_by_result = {}

    # Open the JSON file
    with open(filename) as file:
        file_json = json.load(file)

    # Iterate over the data to count judge results for each error
    for envio_id, cases in file_json.items():
        for case_num, case_info in cases.items():
            # Try to convert case_num to int, if fails, continue with the next case
            try:
                case_num = int(case_num)
            except ValueError:
                continue
            
            errors = case_info.get("list_errors", [])
            result = case_info.get("judge_result", "")

            # Add each error to the list corresponding to the judge result
            for error in errors:
                if error not in errors_by_result:
                    errors_by_result[error] = {"total_cases": 0, "results": {}}

                if result not in errors_by_result[error]["results"]:
                    errors_by_result[error]["results"][result] = 0
                
                errors_by_result[error]["results"][result] += 1
                errors_by_result[error]["total_cases"] += 1

    # Print the results
    for error, data in errors_by_result.items():
        print("Error:", error)
        total_cases_error = data["total_cases"]
        for result, count in data["results"].items():
            percentage = (count / total_cases_error) * 100
            print(f"{result}, Count: {count}, Percentage: {percentage:.2f}%")



if __name__ == '__main__':
    #parseLogs('asan_todos', 'ubsan.log', 'todos_ubsan_orden.json')
    count_errorsUbsan('todos_ubsan.json')
    #count_result('todos_ubsan.json')
    #si dos errores van siempre de la mano los podemos contar como solo un id


