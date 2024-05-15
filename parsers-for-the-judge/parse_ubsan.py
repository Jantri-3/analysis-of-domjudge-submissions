import re
import sys


#Get the number of tries of the students
tries = int(sys.argv[1])

#Establish number of tries to get determined information
superficialInfo = True #Will include only the id of the error
information = False #Will include the id of the problem and if exists, the location
inDepthInfo = False #Will include the id of the problem the message and if exists, the location

if tries == 1: 
    information = True
elif tries > 1:
    information = True
    inDepthInfo = True
    

# Function to parse log of ubsan
def parse_log(log_file):
    with open(log_file,'r') as src:
    # We do not check if the file exists as in DOMJudge enviroment this can be taken as granted 
    # Open the output file (append to not overwrite if the other tools output are ran previously to this one)
        with open("teammessage.txt", "a") as output_file: 
            if src.tell != 0:
                output_file.write("Errors detected by Ubsan: \n")
            for line in src:
                if line == '\n':
                    continue
                try:

                    error = line.split(':')[4]
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
                       
                # Get the corresponding information of the error
                error_id = error
                if information:
                    line_number = line.split(':')[1]
                    column_number = line.split(':')[2]
                if inDepthInfo:
                    message = (":".join(line.split(':')[4::]))
                

                # Write error information to output file
                output_file.write(f"Error ID: {error_id}\n")
                if inDepthInfo:
                    output_file.write(f"Message: {message}\n")
                if information:
                    output_file.write(f"Location of the error: Line: {line_number}, Column: {column_number}\n")
                output_file.write("\n")


# Path to the ubsan log file
log_file_path = 'ubsan.log'


# Call the function to parse ubsan log and generate output
parse_log(log_file_path)