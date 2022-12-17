import configparser
import openai

def _read_api_key():
    config = configparser.ConfigParser()
    config.read('.aexconfig')
    return config

def edit(about_this, output_path=None, model = "code-davinci-edit-001", temperature=0.5, silent=False, stop='===================\n'):
    config = _read_api_key()
    openai.api_key = config['openai']['openai_key']

    completions = openai.Edit.create(engine=model, input=about_this, instruction="Add a detailed paragraph at the top of the code describing what the whole code is doing, and add detailed comments explaining every class and function, including parameters received", temperature=temperature, top_p=0.2, stop=stop)

    text = completions.choices[0].text
    if output_path:
        if not silent:
            print(text)
            user_input = input("Save documentation result? [Y/n] ")
            if user_input.lower() not in ["y", "yes", "", "Y"]:
                return None
        with open(output_path, 'w') as f:
            f.write(text)
            f.close()
    return text

def complete(prompt, output_path=None, model = "code-davinci-001", temperature=0.5, num_tokens=1024, silent=False):
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
                    print('\nThe generated README is not saved.')
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
