switcher = {
    'stack-overflow': 'A stack overflow was detected, this usually means too many recursive calls were made.',
    'heap-buffer-overflow':
        'A heap overflow was detected, this is usually due to an out of bounds array access but can also be caused'
        ' by repeated or big memory allocations using the malloc function or the new keyword.',
    'SEGV': 'A segmentation fault was detected, it is caused by accessing a portion of memory that does not belong'
            ' to the program, some common causes are null pointer dereferencing, dangling pointers (they point to a'
            ' variable that no longer exists), and writes to read-only memory portions.',
    'stack-use-after-return': 'The program accessed an address referencing a local variable that was deleted after'
                              ' returning from a function.',
    'detected memory leaks': 'The program has memory leaks, they are caused by losing reference to dynamically'
                             ' allocated memory.',
    'heap-use-after-free': 'The program is accesing dynamically allocated memory that was already freed.',
    'global-buffer-overflow': 'A global buffer overflow was detected, it is usually caused by an out of bounds access'
                              ' to a global array.'
}

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
        message = switcher.get(error)
        if message is not None:
            with open('teammessage.txt', 'a') as output_file:
                output_file.write(message + '\n')
