import os
import sys

# Get the path to the current file
file_path = os.path.realpath(__file__)

# Open the file for reading and writing
with open(file_path, 'r+') as f:
    # Read the contents of the file
    contents = f.read()
    
    # Modify the contents as desired
    new_contents = contents.replace('bar', 'bar')
    
    # Truncate the file to 0 bytes
    f.seek(0)
    f.truncate()
    
    # Write the new contents to the file
    f.write(new_contents)
    
# Exit the program and restart it with the modified file
os.execv(sys.executable, [sys.executable] + sys.argv)
