# Source :https://github.com/earthlab/autograding-notebooks/tree/master/scripts

# Create template repo for github classroom from released notebooks
# for assignment in nbgrader directory; (fails if template dir already exists)

# Template repo with name assignment-template must already exist in
# GitHub organization

import sys
import os
import fnmatch
import argparse
import subprocess
import shutil


def add_gitignore(repo_name):
    """ Adds .gitignore file to repository before pushing to Classroom. """
    filename = os.path.join(repo_name, '.gitignore')
    with open(filename, 'w') as f:
        f.write(".DStore\n")
        f.write(".ipynb_checkpoints\n")


def add_readme(repo_name, assignment, script_root):
    """ Create a stub of a readme file for the template repo."""

    print("Creating readme")

    readme_template = os.path.join(script_root, 'README_template')
    with open(readme_template, 'r') as f:
        readme_txt = f.read()
        readme_txt.replace('<<ASSIGNMENT>>', assignment)

    filename = os.path.join(repo_name, 'readme.md')
    with open(filename, 'w') as f:
        f.write(readme_txt)


def get_notebooks(nbgrader_dir, assignment):
    """ Get the list of notebooks for this assignment assumes assignemnts
        have been released (i.e. are in release dir).

    """

    print("Getting notebooks")
    release_dir = os.path.join(nbgrader_dir, 'release', assignment)
    notebooks = []
    for file in os.listdir(release_dir):
        if fnmatch.fnmatch(file, '*.ipynb'):
            print(file)
            notebooks.append(file)
    print("Found {} notebooks".format(len(notebooks)))
    return notebooks


def do_local_git_things(repo_name):
    """ Does all of the local git things but does not push to github.

    """

    git = ['git', '-C', repo_name]
    try:
        if not os.path.exists(os.path.join(repo_name,'.git')):
            print("initializing git repo")
            subprocess.check_output(git + ['init'])
        for file in os.listdir(repo_name):
            if fnmatch.fnmatch(file, '*.ipynb'):
                subprocess.check_call(git + ['add', file])
        subprocess.check_output(git + ['commit', '-mInitial commit'])
    except subprocess.CalledProcessError as e:
        print(e.output)
        print('One or more git actions failed; exiting')


def push_to_github(org_name,repo_name):
    """ Push to the github classroom org:
        git remote add origin git@github.com:earth-analytics-edu/repo_name.git
        git push -u origin master

    """

    repo_url = "git@github.com:{}/{}.git".format(org_name,repo_name)
    git = ['git', '-C', repo_name]

    try:
        print("pushing to github repo {}".format(repo_url))
        subprocess.check_output(git + ['remote','add','origin',repo_url])
        subprocess.check_output(git + ['push','-u','origin','master'])
    except subprocess.CalledProcessError as e:
        print(e.output)
        print('Git push failed')


if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',
        help="Whether to {create} local repo, {push} to github, or both",
        choices=["create", "push", "both"],
        default="both",
        nargs='?',
        )
    parser.add_argument('nbgrader_dir', help='path to nbgrader directory')
    parser.add_argument('assignment', help='assignment name, e.g., "2019-01-31-stability" or "ea-04-bootcamp-spatial-data"')
    parser.add_argument('--org_name', help='name of GitHub Classroom organization; default = earth-analytics-edu', default="earth-analytics-edu")
    args = parser.parse_args()

    # notebooks = get_notebooks(args.nbgrader_dir, args.assignment)
    # cp notebooks to new dir and initialize as git repo
    assignment = args.assignment
    repo_name = assignment + '-template'
    mode = args.mode

    # Create directory and populate with files
    if (mode == 'create' or mode == 'both'):
        try:
            os.mkdir(repo_name)
            print("Creating new directory at {}".format(repo_name))
        except FileExistsError as fee:
            print("directory {} already exists; exiting".format(repo_name))
            sys.exit(1)

        # copy notebooks to repo
        print("Getting notebooks")
        release_dir = os.path.join(args.nbgrader_dir,'release', assignment)
        nbooks = 0
        for file in os.listdir(release_dir):
            if fnmatch.fnmatch(file, '*.ipynb'):
                nb = os.path.join(release_dir,file)
                print("copying {} to {}".format(nb,repo_name))
                shutil.copy(nb,repo_name)
                nbooks += 1
        print("Copied {} notebooks".format(nbooks))

        add_readme(repo_name, assignment)
        add_gitignore(repo_name)
        do_local_git_things(repo_name)

    # Push to github
    if (mode == 'push' or mode == 'both'):
        push_to_github(args.org_name,repo_name)
