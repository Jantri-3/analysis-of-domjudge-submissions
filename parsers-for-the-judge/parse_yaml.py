import sys
import yaml


def fun(x, y):
    pass


switcher = {'performance-avoid-endl': lambda x, y: avoidendl(x, y),
            'bugprone-narrowing-conversions': lambda x, y: narrow(x, y),
            'performance-for-range-copy': lambda x, y: rangecopy(x, y),
            'performance-unnecessary-value-param': lambda x, y: valueparam(x, y),
            'bugprone-branch-clone': lambda x, y: branchclone(x, y),
            'bugprone-integer-division': lambda x, y: intdiv(x, y),
            'bugprone-suspicious-semicolon': lambda x, y: sussemicolon(x, y),
            'misc-redundant-expression': lambda x, y: redund(x, y)}


def avoidendl(num, error_tidy):
    if num == 0:
        return'Try avoiding endl'
    elif num == 1:
        return'Instead of endl you can use "\\n"'
    else:
        return 'Instead of endl you should use "\\n", endl can cause errors as it flushes the output buffer, ' \
              'it is also less performant, as it makes more unnecessary input operations'


def narrow(num, error_tidy):
    if num == 0:
        return'Try avoiding operating between different types as it can cause unexpected behavior'
    else:
        return error_tidy['DiagnosticMessage']['Message'], 'this is best avoided as it can lead to unexpected behavior'


def rangecopy(num, error_tidy):
    if num == 0:
        return'When using for each loops you should avoid copying data when you do not need to'
    elif num == 1:
        return'If you use a for each loop be careful not to use expensive data types without const reference ' \
              'as a loop variable.'
    else:
        return'If you use a for each loop be careful not to use expensive data types without const reference ' \
              'as a loop variable as it can be expensive to copy'


def valueparam(num, error_tidy):
    if num == 0:
        return'You should be careful when passing expensive to copy data types as an argument'
    elif num == 1:
        return'You should pass arguments of expensive to copy data types by reference instead of copying them'
    else:
        returnerror_tidy['DiagnosticMessage']['Message']


def branchclone(num, error_tidy):
    if num == 0:
        return'There are repeated branches in your code'
    elif num == 1:
        return'Be careful with your conditional statements as you might have repeated some branches'
    else:
        return'Be careful with your conditional statements as you might have repeated some branches' \
              'check if/else and switch statements that you might have copy-pasted'


def intdiv(num, error_tidy):
    if num == 0:
        return'You are losing precision with integer division. Is that intended?'
    elif num == 1:
        return'The result of integer division is possibly truncated before conversion'
    else:
        return'Check your integer divisions as you might be truncating the result before' \
              'converting to double/float. For example: double d = 3/2 resolves to 1 and then' \
              'it is casted to double, instead of the expected 1.5 you get 1.0'


def sussemicolon(num, error_tidy):
    if num == 0:
        return'There are suspicious semicolons in your code'
    elif num == 1:
        return'Be careful with if/while/for with a semicolon after the condition'
    else:
        return'Be careful with if/while/for with a semicolon after the condition' \
              'as it can make the following code behave unexpectedly:' \
              ' it can execute unconditionally or execute just once'


def redund(num, error_tidy):
    if num == 0:
        return'There are redundant conditions in your code'
    else:
        return'There are redundant conditions in your code, check your conditional statements as you might have' \
              'copy-pasted something or review the logic for the boolean operators you have used'


if __name__ == '__main__':
    errorsNotFound = True
    tries = int(sys.argv[1])
    with open('clangtidy.yaml', ) as input_file:
        yaml_input = yaml.safe_load(input_file)

    with open("teammessage.txt", "a") as output_file:
        for error in yaml_input['Diagnostics']:
            function = switcher.get(error['DiagnosticName'])
            if function is not None:
                if errorsNotFound:
                    output_file.write('Errors detected by Clang-tidy: \n')
                    errorsNotFound = False
                message = function(tries, error)
                output_file.write('Error ID: ' + error['DiagnosticName'] + '\n')
                output_file.write('Message: ' + message + '\n')
