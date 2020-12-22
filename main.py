import os
import time
import subprocess
import git
import logging


class GitPuller(object):
    def __init__(self):
        super(GitPuller, self).__init__()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='log.log')
        self.__main_work_flow()

    def __main_work_flow(self):
        print('Starting work')
        logging.info('Starting work')
        while True:
            paths = self.__find_git_directories()
            out = [self.__manage_update(x) for x in paths]
            if True in out:
                logging.info('Attempt to the reboot')
                print('Attempt to the reboot the machine')
                os.system('reboot now')
            else:
                print('Nothing found to update, sleeping')
                logging.info('Nothing found to update, sleeping')
            time.sleep(15)

    @staticmethod
    def __find_git_directories():
        paths = subprocess.run(['find', '/', '-type', 'd', '-name', '.git'], stdout=subprocess.PIPE)
        paths = paths.stdout.decode('UTF-8')
        paths = paths.split('\n')
        paths = [x for x in paths if x]
        paths = [print(x) for x in paths]
        return paths

    @staticmethod
    def __manage_update(path):
        path = os.path.split(path)[0]
        os.chdir(path)
        repo = git.Repo(os.getcwd())
        if repo.is_dirty(untracked_files=False):
            t = repo.head.commit.tree
            z = repo.git.diff(t)
            print('Differences\n\n' + z + '\n\n')
            os.system('git reset --hard HEAD')
            logging.info('Differences\n\n' + z + '\n\n')
            time.sleep(1)
            print('Pulling')
            logging.info('Pulling')
            repo.remotes.origin.pull()
            time.sleep(1.5)
            return True


if __name__ == '__main__':
    GitPuller()

# fake comment