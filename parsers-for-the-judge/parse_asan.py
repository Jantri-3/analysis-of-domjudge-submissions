with open('asan.log') as input_file:
    lines = input_file.readlines()
    asan_output_found = False
    error_line_index = 0
    for i, line in enumerate(lines):
        if line.startswith('================================================================='):
            error_line_index = i + 1
            asan_output_found = True

    if asan_output_found:
        error_line = lines[error_line_index].split(':')
        index = 31
        if error_line[1] == ' AddressSanitizer':
            index = 34
        error = error_line[2]
        index = error.find(' on')
        error = error[1:index]

        with open('teammessage.txt', 'a') as output_file:
            output_file.write('ErrorId: ' + error + '\n\n')

