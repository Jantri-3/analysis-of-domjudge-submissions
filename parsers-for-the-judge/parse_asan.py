with open('asan.log', ) as input_file:
    lines = input_file.readlines()
    error_line_index = 0
    for i, line in enumerate(lines):
        if line.startswith('================================================================='):
            error_line_index = i + 1
    index = 31
    error_line = lines[error_line_index].split(':')
    if error_line[1] == ' AddressSanitizer':
        index = 34
    error = error_line[2]
    index = error.find(' on')
    error = error[1:index]

with open('teammessage.txt', 'a') as output_file:
    output_file.write('Error detected by Asan: \n')
    output_file.write('ErrorId: ' + error + '\n\n')

