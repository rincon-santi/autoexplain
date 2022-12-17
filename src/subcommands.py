from src.openai_functions import edit, complete
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
    This function is used to add files to the repository. It takes in a list of files and adds them to the repository, documenting them
    Parameters:
    args: The arguments passed to the add command
    """
    # Iterate over the list of modified files and pass each file to the edit function
    files = args.files
    max = len(files)
    pointer = 0
    while pointer < max:
        if os.path.isdir(files[pointer]):
            files = files + [files[pointer]+file for file in os.listdir(files[pointer])]
            max+=len(os.listdir(files[pointer]))
        else:
            with open(files[pointer], 'r') as f:
                content = f.read()
            edit(content, output_path=files[pointer], silent=args.silent)
        pointer+=1
    if not args.no_stage:
        subprocess.run(["git", "add"]+files)

def generate_readme():
    """
    This function is used to generate a readme file for the repository. It uses the openai API to generate a readme file
    """
    FILES_NOT_TO_INCLUDE = ['LICENSE', 'README.md']
    if os.path.exists('.aexignore'):
        with open('.aexignore', 'r') as f:
            contents = f.read()
        FILES_NOT_TO_INCLUDE = contents.split('\\n')
    cur_dir_not_full_path = os.getcwd().split('/')[-1]
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
        for filename in files_sorted_by_mod_date:
            # Check if file is a image file.
            is_image_file = False
            for extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']:
                if filename.endswith(extension):
                    is_image_file = True
                    break
            if filename not in FILES_NOT_TO_INCLUDE and not filename.startswith('.') \
                    and not os.path.isdir(filename) and not is_image_file:
                with open(filename) as f:
                    input_prompt += '\n===================\n# ' + filename + ':\n'
                    input_prompt += f.read() + '\n'

        input_prompt = input_prompt[:length]
        input_prompt += '\n\n===================\n# ' + 'README.md:' + '\n'
        input_prompt += README_START
        return input_prompt

    prompt = generate_prompt()
    complete(prompt, output_path="README.md")
    

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
