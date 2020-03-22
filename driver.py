import subprocess
from multiprocessing import Pool


def run_script(path):
    subprocess.call(['python3', path])


if __name__ == '__main__':
    subprocess.call(['git', 'reset', '--hard'])
    subprocess.call(['git', 'pull'])

    scripts = ['web_server/app.py', 'slam/app.py']
    pool = Pool(len(scripts))
    pool.map(run_script, scripts)
