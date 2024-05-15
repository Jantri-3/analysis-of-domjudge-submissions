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
            if error.attrib['id'] not in errores_relevantes_cppcheck:
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
            output_file.write(f"Error ID: {error_id}\n")
            if inDepthInfo:
                output_file.write(f"Message: {message}\n")
            if locationExists:
                output_file.write(f"Location of the error: Line: {line_number}, Column: {column_number}\n")
            output_file.write("\n")


# Path to the XML file
xml_file_path = 'cppcheck.xml'

# Relevant errors of Cppcheck
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

# Call the function to parse XML and generate output
parse_xml(xml_file_path)