from os.path import dirname, join

from ml_logger import RUN, instr
from termcolor import colored

assert instr  # single-entry for the instrumentation thunk factory
RUN.script_root = dirname(__file__)
RUN.project = "diffuser"  # Specify the project name
RUN.prefix = "{project}/{file_stem}/{job_name}"