import os
import time
import subprocess


class GitPuller(object):
    def __init__(self):
        super(GitPuller, self).__init__()
        self.__main_work_flow()

    def __main_work_flow(self):
        while True:
            time.sleep(15)
            paths = self.__find_git_directories()
            [self.__manage_update(x) for x in paths]

    @staticmethod
    def __find_git_directories():
        paths = subprocess.run(['find', '/', '-type', 'd', '-name', '.git'], stdout=subprocess.PIPE)
        paths = paths.stdout.decode('UTF-8')
        paths = paths.split('\n')
        paths = [x for x in paths if x]
        return paths

    @staticmethod
    def __manage_update(path):
        path = os.path.split(path)[0]
        os.chdir(path)
        os.system('git pull')


if __name__ == '__main__':
    GitPuller()
