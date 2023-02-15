"""
			This module contains functions for reading an OpenAI API key from a configuration file and for editing and completing text using OpenAI's GPT-3 model.
			
			_read_api_key():
			    Reads an OpenAI API key from a configuration file.
			
			
"""
import configparser
import openai
import difflib


def _read_api_key():
    config = configparser.ConfigParser()
    config.read('.aexconfig')
    return config

def edit(about_this, output_path=None, model = "code-davinci-edit-001", temperature=0.5, silent=False):
    """edit(about_this, output_path=None, model="code-davinci-edit-001", temperature=0.5, silent=False, stop='===================\n'):
			    Uses the OpenAI GPT-3 model to edit a given text.
			    Parameters:
			        about_this (str): The text to be edited.
			        output_path (str): The path to save the edited text.
			        model (str): The OpenAI GPT-3 model to use.
			        temperature (float): The temperature of the model.
			        silent (bool): Whether to print the edited text and ask for confirmation.
			        stop (str): The string to indicate the end of the text
    """
    config = _read_api_key()
    openai.api_key = config['openai']['openai_key']

    completions = openai.Edit.create(engine=model, input=about_this, instruction="Add a detailed paragraph at the top of the code describing what the whole code is doing, and add detailed comments explaining every class and function, including parameters received. Don't modify code.", temperature=temperature, top_p=0.2)

    text = completions.choices[0].text
    if output_path:
        if not silent:
            print("\n-------------------{}-----------------\n\n".format(output_path))
            diff = difflib.unified_diff(about_this.splitlines(), text.splitlines())
            print('\n'.join(diff))
            user_input = input("Save result? [Y/n] ")
            if user_input.lower() not in ["y", "yes", "", "Y"]:
                return None
        with open(output_path, 'w') as f:
            f.write(text)
            f.close()
    return text
				
def complete(prompt, output_path=None, model = "code-davinci-001", temperature=0.5, num_tokens=1024, silent=False):
    """
    Generates a completion for a given prompt using OpenAI's API.
		Args:
		prompt (str): The prompt to generate a completion for.
		output_path (str, optional): The path to save the generated completion to.
		model (str, optional): The OpenAI model to use for generating the completion.
		temperature (float, optional): The temperature to use for generating the completion.
		num_tokens (int, optional): The maximum number of tokens to generate.
	    silent (bool, optional): Whether to print the generated completion or not.
				
		Returns:
			str: The generated completion.
	"""
    config = _read_api_key()
    openai.api_key = config['openai']['openai_key']

    while True:
        text = openai.Completion.create(engine=model, prompt=prompt, temperature=temperature, max_tokens=num_tokens, stream=True, stop='===================\n')
        generated = ''
        while True:
            next_response = next(text)
            completion = next_response['choices'][0]['text']
            generated = generated + completion
            if next_response['choices'][0]['finish_reason'] != None: break
        if output_path:
            if not silent:
                print(generated)
                answer = input("\n\nDo you want to save? [y/N] ")
                if answer == '' or answer == 'n' or answer == 'N':
                    print('\nNot saved.')
                    answer = input("\n\nDo you want to generate another? [Y/n] ")
                    if answer == '' or answer == 'y' or answer == 'Y':
                        continue
                    return generated
                elif answer == 'y' or answer == 'Y':
                    with open(output_path, 'w') as f:
                        f.write(generated)
                    return generated
            else:
                with open(output_path, 'w') as f:
                    f.write(generated)
                return generated
