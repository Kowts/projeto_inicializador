import os
import subprocess
import logging
import argparse

def create_project_directory(project_name, create_docs=True, create_tests=True, create_notebooks=True, create_data=True, create_scripts=True, init_git=True, setup_venv=True, dependencies=None):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.info(f'Created directory: {directory}')
    except OSError as e:
        logging.error(f"Error creating directory {directory}: {e}")

    # Create some initial files with content
    init_files = [
        (f'{project_name}/src/{project_name}/__init__.py', '# Initialization file for the project package.\n'),
        (f'{project_name}/README.md', generate_readme_content(project_name)),
        (f'{project_name}/LICENSE', generate_license_content()),
        (f'{project_name}/requirements.txt', ''),
        (f'{project_name}/.env', generate_env_content()),
        (f'{project_name}/setup.py', generate_setup_script_content(project_name))
    ]

    if create_scripts:
        init_files.append((f'{project_name}/scripts/__init__.py', ''))
    if create_tests:
        init_files.append((f'{project_name}/tests/__init__.py', ''))

    try:
        for file_path, content in init_files:
            with open(file_path, 'w') as f:
                f.write(content)
            logging.info(f'Created file: {file_path} with initial content')
    except OSError as e:
        logging.error(f"Error creating file {file_path}: {e}")

    # Initialize Git repository if requested
    if init_git:
        initialize_git_repo(project_name)

    # Set up virtual environment if requested
    if setup_venv:
        setup_virtual_environment(project_name)
        if dependencies:
            install_dependencies(project_name, dependencies)

def generate_readme_content(project_name):
    return f"""# {project_name}

Este projeto é uma estrutura básica para iniciar o desenvolvimento de aplicações Python. Ele inclui diretórios para código-fonte, testes, documentação, dados, notebooks, e scripts auxiliares.

## Estrutura do Projeto

- `src/`: Código-fonte do projeto.
- `tests/`: Testes automatizados.
- `docs/`: Documentação do projeto.
- `data/`: Dados necessários para o projeto.
- `notebooks/`: Notebooks Jupyter para experimentação e prototipagem.
- `scripts/`: Scripts auxiliares e utilitários.

## Como Utilizar

1. Clone este repositório para sua máquina local.
2. Modifique os arquivos e diretórios conforme necessário.
3. Desenvolva seu projeto seguindo a estrutura estabelecida.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
"""

def generate_license_content():
    return """MIT License

Copyright (c) 2024 [Seu Nome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def generate_env_content():
    return """# Environment variables for the project
# Example:
# SECRET_KEY=your-secret-key
"""

def generate_setup_script_content(project_name):
    return f"""import os
from dotenv import load_dotenv
import subprocess
import sys

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Activate virtual environment
    activate_venv()

    # Install dependencies from requirements.txt
    install_dependencies()

def activate_venv():
    venv_path = os.path.join(os.getcwd(), 'venv')
    if os.name == 'nt':
        activate_script = os.path.join(venv_path, 'Scripts', 'activate')
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')

    if os.path.exists(activate_script):
        print(f'Activating virtual environment from {activate_script}')
        subprocess.run([activate_script], shell=True)
    else:
        print('Virtual environment not found. Please set it up manually.')

def install_dependencies():
    requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.exists(requirements_path):
        print(f'Installing dependencies from {requirements_path}')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
    else:
        print('No requirements.txt found.')

if __name__ == '__main__':
    main()
"""

def initialize_git_repo(project_name):
    try:
        subprocess.run(["git", "init", project_name], check=True)
        logging.info('Initialized a new Git repository.')
        
        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Packages
*.egg
*.egg-info/
dist/
build/
eggs/
parts/
var/
sdist/
develop-eggs/
.installed.cfg
lib/
lib64/
*.dist-info/

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Virtual environments
venv/
ENV/
env/
.venv/
env.bak/
.env.bak/
.venv.bak/
venv.bak/

# Pyre type checker
.pyre/
"""
        with open(os.path.join(project_name, '.gitignore'), 'w') as f:
            f.write(gitignore_content)
        logging.info('Created .gitignore file.')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error initializing Git repository: {e}")

def setup_virtual_environment(project_name):
    try:
        venv_path = os.path.join(project_name, 'venv')
        subprocess.run(["python3", "-m", "venv", venv_path], check=True)
        logging.info(f'Virtual environment created at {venv_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting up virtual environment: {e}")

def install_dependencies(project_name, dependencies):
    venv_path = os.path.join(project_name, 'venv', 'bin', 'pip')
    try:
        subprocess.run([venv_path, "install"] + dependencies, check=True)
        logging.info(f'Installed dependencies: {", ".join(dependencies)}')
        with open(f'{project_name}/requirements.txt', 'w') as f:
            f.write("\n".join(dependencies))
        logging.info('Created requirements.txt with specified dependencies.')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialize a new Python project.")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--no-docs", action="store_false", dest="create_docs", help="Don't create a docs directory")
    parser.add_argument("--no-tests", action="store_false", dest="create_tests", help="Don't create a tests directory")
    parser.add_argument("--no-notebooks", action="store_false", dest="create_notebooks", help="Don't create a notebooks directory")
    parser.add_argument("--no-data", action="store_false", dest="create_data", help="Don't create a data directory")
    parser.add_argument("--no-scripts", action="store_false", dest="create_scripts", help="Don't create a scripts directory")
    parser.add_argument("--no-git", action="store_false", dest="init_git", help="Don't initialize a Git repository")
    parser.add_argument("--no-venv", action="store_false", dest="setup_venv", help="Don't set up a virtual environment")
    parser.add_argument("--dependencies", nargs='+', help="List of Python packages to install in the virtual environment")

    args = parser.parse_args()

    create_project_directory(
        project_name=args.project_name,
        create_docs=args.create_docs,
        create_tests=args.create_tests,
        create_notebooks=args.create_notebooks,
        create_data=args.create_data,
        create_scripts=args.create_scripts,
        init_git=args.init_git,
        setup_venv=args.setup_venv,
        dependencies=args.dependencies
    )
