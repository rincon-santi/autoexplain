import subprocess

def is_file_staged(filename):
    result = subprocess.run(['git', 'diff', '--name-only'], stdout=subprocess.PIPE)
    changed_files = result.stdout.decode().strip().split('\n')
    return filename not in changed_files