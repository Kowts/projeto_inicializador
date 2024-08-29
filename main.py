import os

def create_project_directory(project_name, create_docs=True, create_tests=True, create_notebooks=True, create_data=True, create_scripts=True):
    # Define the directory structure
    directories = [
        f'{project_name}/',
        f'{project_name}/src/{project_name}'
    ]
    
    if create_docs:
        directories.append(f'{project_name}/docs')
    if create_tests:
        directories.append(f'{project_name}/tests')
    if create_data:
        directories.append(f'{project_name}/data')
    if create_notebooks:
        directories.append(f'{project_name}/notebooks')
    if create_scripts:
        directories.append(f'{project_name}/scripts')

    # Create the directories
    try:
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f'Created directory: {directory}')
    except OSError as e:
        print(f"Error creating directory {directory}: {e}")

    # Create some initial files with content
    init_files = [
        (f'{project_name}/src/{project_name}/__init__.py', '# Initialization file for the project package.\n'),
        (f'{project_name}/README.md', f'# {project_name}\n\nA brief description of your project.\n')
    ]
    
    if create_scripts:
        init_files.append((f'{project_name}/scripts/__init__.py', ''))
    if create_tests:
        init_files.append((f'{project_name}/tests/__init__.py', ''))

    try:
        for file_path, content in init_files:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f'Created file: {file_path} with initial content')
    except OSError as e:
        print(f"Error creating file {file_path}: {e}")

if __name__ == '__main__':
    project_name = 'MyEnhancedPythonProject'
    create_project_directory(project_name, create_docs=True, create_tests=True, create_notebooks=True, create_data=True, create_scripts=True)
