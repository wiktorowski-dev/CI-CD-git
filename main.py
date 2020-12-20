import os
import time


class GitPuller(object):
    def __init__(self):
        super(GitPuller, self).__init__()

    def __main_work_flow(self):
        while True:
            time.sleep(5)
            paths = self.__find_git_directories()
            [self.__manage_update(x) for x in paths]


if __name__ == '__main__':
    GitPuller()
