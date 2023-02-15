from src.functions.openai_functions import edit, complete
from src.constants.aexp_constants import NOT_INCLUDED_PREFIXES, NOT_INCLUDED_EXTENSIONS, FILES_NOT_TO_INCLUDE
from src.utils.utils import is_file_staged
from src.constants.prompts import GENERATE_UNITTEST_PROMPT
import subprocess
import configparser
import os

"""
This file contains all the functions that are used to interact with the files in the repository
It contains the following functions:
add: This function is used to add files to the repository. It takes in a list of files and adds them to the repository, documenting them
generate_readme: This function is used to generate a readme file for the repository. It uses the openai API to generate a readme file
set_key: This function is used to set the openai API key. It takes in the key as an argument and stores it in the .aexconfig file
"""

def add(args):
    """
    This function is used to add files to the repository. It takes in a list of files and adds them to the repository, documenting them.
    It also adds the files to the staging area.
    Parameters:
    args: The arguments passed to the add command
    """
    # Iterate over the list of modified files and pass each file to the edit function
    def _conditions(filename, path): # This function is used to check if the file is to be included in the repository.
        for extension in NOT_INCLUDED_EXTENSIONS:
            if filename.endswith(extension):
                return False
        for prefix in NOT_INCLUDED_PREFIXES:
            if filename.startswith(prefix):
                return False
        if is_file_staged(path+filename):
            return False
        return True

    files = args.files # This is the list of files that are to be added to the repository
    max_files = len(files)
    pointer = 0
    while pointer < max_files: # Iterate over the list of files
        if os.path.isdir(files[pointer]):
            included_files = [files[pointer]+file for file in os.listdir(files[pointer]) if _conditions(file, files[pointer])] # If the file is a directory, add all the files in the directory to the list of files to be added
            files = files + included_files
            max_files+=len(included_files)
        else:
            with open(files[pointer], 'r') as f: # If the file is not a directory, open the file and pass it to the edit function
                content = f.read()
            edit(content, output_path=files[pointer], silent=args.silent)
        pointer+=1
    if not args.no_stage: # If the --no-stage flag is not passed, add the files to the staging area
        subprocess.run(["git", "add"]+files)

def generate_readme(output_file="README.md", silent=False):
    """
    This function is used to generate a readme file for the repository. It uses the openai API to generate a readme file
    """
    ignored = FILES_NOT_TO_INCLUDE # This is the list of files that are not to be included in the readme file
    if os.path.exists('.aexignore'):
        with open('.aexignore', 'r') as f: # If the .aexignore file exists, read the contents of the file and add them to the list of files not to be included in the readme file
            contents = f.read()
        ignored = contents.split('\\n')
    cur_dir_not_full_path = os.getcwd().split('/')[-1] # This is the name of the current directory
    README_START =  f'# {cur_dir_not_full_path}\n## What is it?\n'

    def generate_prompt(length=3000):
        """
        This function has been borrowed from tom-doerr (https://github.com/tom-doerr/codex-readme)
        Parameters:
        length: The length of the prompt to be generated
        """
        input_prompt = ''
        files_sorted_by_mod_date = sorted(os.listdir('.'), key=os.path.getmtime)
        # Reverse sorted files.
        files_sorted_by_mod_date = files_sorted_by_mod_date[::-1]
        for filename in files_sorted_by_mod_date: # Iterate over the list of files in the directory
            # Check if file is a image file.
            is_image_file = False
            for extension in NOT_INCLUDED_EXTENSIONS:
                if filename.endswith(extension):
                    is_image_file = True
                    break
            if filename not in ignored and not filename.startswith('.') \
                    and not os.path.isdir(filename) and not is_image_file:
                with open(filename) as f: # If the file is not to be ignored, open the file and add it to the prompt
                    input_prompt += '\n===================\n# ' + filename + ':\n'
                    input_prompt += f.read() + '\n'

        input_prompt = input_prompt[:length]
        input_prompt += '\n\n===================\n# ' + 'README.md:' + '\n'
        input_prompt += README_START
        return input_prompt

    prompt = generate_prompt()
    complete(prompt, output_path=output_file, silent=silent)

def generate_unittests(files, silent=False):
    with open(files[0], 'r') as f: 
        content = f.read()
    prompt = GENERATE_UNITTEST_PROMPT.format(content=content, code_file=files[0])
    complete(prompt, output_path=files[1], silent=silent)

def set_key(args):
    """
    This function is used to set the openai API key. It takes in the key as an argument and stores it in the .aexconfig file
    Parameters:
    args: The arguments passed to the set_key command
    """
    config = configparser.ConfigParser()
    config.read('.aexconfig')
    if not config.has_section('openai'):
        config.add_section('openai')
        with open('.gitignore', 'a') as gitignorefile:
            gitignorefile.write('\\n.aexconfig')
    config.set('openai', 'openai_key', args.key[0])
    with open('.aexconfig', 'w') as configfile:
        config.write(configfile)
