import subprocess
from multiprocessing import Pool


def run_script(path):
    subprocess.call(['python3', path])


if __name__ == '__main__':
    # pull from repo
    subprocess.call(['git', 'reset', '--hard'])
    subprocess.call(['git', 'pull'])

    # install any missing requirements
    subprocess.call(['pip3', 'install', '-r', 'web_server/requirements.txt'])

    # run scripts as separate processes
    scripts = ['web_server/app.py', 'slam/app.py']
    pool = Pool(len(scripts))
    pool.map(run_script, scripts)
