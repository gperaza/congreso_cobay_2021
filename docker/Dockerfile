FROM python:3

# Install nbgrader
RUN pip install jupyter
RUN pip install nbgrader

# Add any other dependencies you might want, e.g. numpy, scipy, etc.
RUN pip install numpy scipy matplotlib scikit-learn pandas seaborn

# Configure grader user
RUN useradd -m grader
RUN chown -R grader:grader /home/grader
USER grader

# Where the assignments will live (these need to be mounted on runtime)
WORKDIR /assignments

ENTRYPOINT ["nbgrader"]
CMD ["--help"]
