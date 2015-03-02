from expr import *
from stmt import *
from decl import *
from base import *


def BuildEnv(ast):
    env_builder = EnvBuilder()
    return env_builder.Visit(ast)
