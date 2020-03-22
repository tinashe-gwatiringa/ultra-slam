import subprocess
from multiprocessing import Pool
import argparse

VERSION = "0.0.0"


def run_script(path):
    subprocess.call(['python3', path])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='ultra-slam v' + str(VERSION))
    parser.add_argument(
        "-p", "--pull", help="pull from repo", action="store_true")
    parser.add_argument(
        "-r", "--requirements", help="install requirements", action="store_true")
    parser.add_argument(
        "-i", "--initialise", help="run initialisation script", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.pull:
        # pull latest from repo
        subprocess.call(['git', 'reset', '--hard'])
        subprocess.call(['git', 'pull'])

    if args.requirements:
        # install using requirements.txt
        subprocess.call(
            ['pip3', 'install', '-r', 'web_server/requirements.txt'])

    if args.initialise:
        # run initialise script
        subprocess.call(['python3', 'web_server/init.py'])

    # run scripts as separate processes
    scripts = ['web_server/app.py', 'slam/app.py']
    pool = Pool(len(scripts))
    pool.map(run_script, scripts)
