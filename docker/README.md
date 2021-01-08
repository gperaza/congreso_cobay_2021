Assuming you are in the directory with the Dockerfile, build the image with:

    docker build -t jupyter/nbgrader .

Then, `cd` to the root of you nbgrader directory and run:

    NBGRADER="docker run --rm -v $(pwd):/assignments/ jupyter/nbgrader"

(This command tells docker to run the `jupyter/nbgrader` image and mount the current directory inside the
container at the path `/assignments`, and to remove the docker container when the command has finished).

Now, you can use `${NBGRADER}` rather than `nbgrader` to run your nbgrader commands, e.g.:

    ${NBGRADER} assign "Problem Set 1"
    ${NBGRADER} autograde "Problem Set 1"

These commands will run nbgrader inside a docker container rather than directly on your machine.
Note that this setup does mount your entire nbgrader directory, so it’s possible for students’
code to remove any files within that nbgrader directory. Thus, you should have those backed up
somewhere before running the autograder. This setup will protect the rest of the files on the
machine, however.