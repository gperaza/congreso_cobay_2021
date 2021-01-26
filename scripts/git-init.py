#!/usr/bin/env python3

# Modified by Gonzalo Peraza 2020

# Script to init a git repo for a lesson template
# Assumes that cwd is the released assignment directory, under release

import os
import shutil
import subprocess


def readme():
    txt = """# README

This repository contains a notebook assignment.
Complete the  homework in each .ipynb notebook, commit your work, and push the changes to github.
Your instructor will pull the completed assignemnt after the deadline.

Once grading is complete, your instructor will push the results to a file called `feedback.html`.
You will need to pull the changes to your local copy and open this file in a browser to view (github will not render html files).
"""

    return txt

def ignore():
    txt = """.DStore
.ipynb_checkpoints
"""

    return txt

if __name__ == '__main__':
    template_dir = '/home/gperaza/Nbgrader/nbgrader-scripts/'

    # readme_file = os.path.join(template_dir, 'README.md')
    # shutil.copyfile(readme_file, os.path.join('.', 'README.md'))
    readme_file = os.path.join('.', 'README.md')
    with open(readme_file, 'w') as f:
        f.write(readme())

    # ignore_file = os.path.join(template_dir, 'gitignore')
    #shutil.copyfile(ignore_file, os.path.join('.', '.gitignore'))
    ignore_file = os.path.join('.', '.gitignore')
    with open(ignore_file, 'w') as f:
        f.write(ignore())

    subprocess.check_output(['git', 'init'])
    subprocess.check_output(['git', 'add', '-A'])
    subprocess.check_output(['git', 'commit', '-mFirst commit'])
