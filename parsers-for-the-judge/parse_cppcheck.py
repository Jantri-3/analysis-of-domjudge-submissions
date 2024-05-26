import xml.etree.ElementTree as ET
import sys


#Get the number of tries of the students
tries = int(sys.argv[1])

#Establish number of tries to get determined information
superficialInfo = True #Will include only the id of the problem
information = False #Will include the id of the problem and if exists, the location
inDepthInfo = False #Will include the id of the problem the message and if exists, the location

if tries == 1: 
    information = True
elif tries > 1:
    superficialInfo = False
    information = True
    inDepthInfo = True
    

# Function to parse Cppcheck XML file
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # We do not check if the file exists as in DOMJudge enviroment this can be taken as granted 
    # Open the output file (append to not overwrite if the other tools output are ran previously to this one)

    errorNotfound = True
    with open("teammessage.txt", "a") as output_file: 
        # Iterate over each error in the XML
        for error in root.findall('.//error'):
            if error.attrib['id'] not in relevant_errors_cppcheck:
                continue
            if errorNotfound:
                output_file.write("Errors detected by Cppcheck: \n")
                errorNotfound = False
            # Get the corresponding information of the error
            locationExists = False
            error_id = error.attrib['id']
            if information:
                location = error.find('location')
                if location is not None:
                    locationExists = True
                    line_number = location.attrib['line']
                    column_number = location.attrib['column']
            if inDepthInfo:
                message = error.attrib['msg']
            

            # Write error information to output file
            if superficialInfo:
                output_file.write(f"Error: {initial_explanation.get(error_id)}\n")
            if inDepthInfo:
                output_file.write(f"Message: {message}\n")
            if locationExists:
                output_file.write(f"Location of the error: Line: {line_number}, Column: {column_number}\n")
            output_file.write("\n")


# Path to the XML file
xml_file_path = 'cppcheck.xml'

# Relevant errors of Cppcheck
relevant_errors_cppcheck = ['uninitvar',
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

#Dictionary messages for the student
initial_explanation = {'uninitvar': "There is an uninitialized variable",
                               'unreadVariable': "There is a variable in your code that during the execution is'nt going to be read",
                               'shadowFunction': "You have one or more than one functions with the same name in different scopes",
                               'shadowVariable': "You have one or more than one variables with the same name in different scopes",
                               'shadowArgument': "You have one or more than one arguments with the same name in different scopes",
                               'knownConditionTrueFalse': "A condition in the code is always true or always false",
                               'redundantCondition': "There is a redundant condition in the code",
                               'multiCondition': "There is an expression which is always true (because of an else if condition being opposite to the first)",
                               'duplicateExpression': "There is a duplicate expression at both sides of a comparison",
                               'duplicateBreak': "There are consecutive breaks in the code (continues, returns,etc)",
                               'uninitStructMember': "A member of an struct is not initialized",
                               'noConstructor': "There is no constructor of a class",
                               'unreachableCode': "Some parts of the code are not reachable",
                               'knownEmptyContainer': "The code iterates a known empty variable",
                               'clarifyCondition': "There is a condition in the code which should be clarified with parenthesis",
                               'selfAssignment': "Redundant assignment of a variable to itself",
                               'negativeContainerIndex': "Either there is a redundant condition or there is a negative array index",
                               'containerOutOfBounds': "Either there is a rendundant condition or an expression is trying to access out of the bounds of a variable",
                               'identicalInnerCondition': "there is an identical inner condition",
                               'passedByValue': "A function parameter could and should be passed as a constant reference",
                               'stlFindInsert': "Searching before insertion in an array is not necessay, consider using ***.tryemplace()",
                               'iterateByValue': "Range variable should be declared as a constant reference",
                               'useInitializationList': "A variable is assigned in the constructor body. Consider performing initialization in the initialization list",
                               'missingReturn': "Found an exit path from a function with non-void return type that has a missing return statement",
                               'legacyUninitvar': "There is an uninitialized variable",
                               'internalAstError': "AST broken, binary operator does not have two operands",
                               'selfInitialization': "A variable is initialized by itself",
                               'constStatement': "Redundant code - constant statement"
}

# Call the function to parse XML and generate output
parse_xml(xml_file_path)