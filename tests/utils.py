import os


class Environment:

    def __init__(self, envs):
        self.envs = envs

    def __enter__(self):
        self.old = os.environ
        os.environ = dict(os.environ, **self.envs)

    def __exit__(self, type, value, traceback):
        os.environ = self.old
