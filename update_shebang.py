import os 
def update_shebang(file_path):
    with open(file_path, 'r') as file: #opening file
        lines = file.readlines()
    if lines[0].startswith('#!'): #checking condition 
        lines[0] = '#!/usr/bin/env python3\n'
    else:
        lines.insert(0, '#!/usr/bin/env python3\n') 
    with open(file_path, 'w') as file: #updating 
        file.writelines(lines)

for root, dirs, files in os.walk('.'): #checking directory for files
    for file in files:
        if file.endswith('.py'): #condition for python files
            update_shebang(os.path.join(root, file))
