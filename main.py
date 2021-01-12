import os
import time
import subprocess
import git
import logging


class GitPuller(object):
    def __init__(self):
        super(GitPuller, self).__init__()
        self.__path_file_exclude = r'exclude_paths.txt'
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='log.log')
        self.__main_work_flow()

    def __main_work_flow(self):
        print('Starting work')
        logging.info('Starting work')
        while True:
            exclude_paths = self.__get_paths_to_exclude()
            paths = self.__find_git_directories(exclude_paths)
            out = [self.__manage_update(x) for x in paths]
            if True in out:
                logging.info('Attempt to the reboot')
                print('Attempt to the reboot the machine')
                os.system('sudo /sbin/shutdown -r now')
            else:
                print('Nothing found to update, sleeping')
                logging.info('Nothing found to update, sleeping')
            time.sleep(15)

    @staticmethod
    def __find_git_directories(exclude_paths):
        paths = subprocess.run(['find', '/', '-type', 'd', '-name', '.git'], stdout=subprocess.PIPE)
        paths = paths.stdout.decode('UTF-8')
        paths = paths.split('\n')
        paths = [x for x in paths if x]
        paths = [x for x in paths if x not in exclude_paths]
        return paths

    def __manage_update(self, path):
        print("Actual working path: {}".format(path))
        path = os.path.split(path)[0]
        os.chdir(path)
        repo = git.Repo(os.getcwd())

        t = repo.head.commit.tree
        z = repo.git.diff(t)
        print('Differences\n' + z + '\n')
        logging.info('Differences\n' + z + '\n')

        try:
            msg_out = subprocess.check_output(['git', 'pull'])
        except:
            msg_out = None

        if not msg_out:
            self.__hard_pull(repo)

        elif 'already up to date' in msg_out.decode('UTF-8').lower():
            print('Nothing to pull')
            logging.info('Nothing to pull')
            return None

        else:
            self.__hard_pull(repo)

        return True

    @staticmethod
    def __hard_pull(repo):
        os.system('git reset --hard HEAD')
        repo.remotes.origin.pull()
        print('Hard pulling')
        logging.warning('Hard pulling')

    def __get_paths_to_exclude(self):
        if os.path.isfile(self.__path_file_exclude):
            with open(self.__path_file_exclude) as file:
                file = file.read()

            paths = file.split('\n')
            paths = [x for x in paths if x]

        else:
            with open(self.__path_file_exclude, mode='a') as file:
                pass

            paths = []

        return paths


if __name__ == '__main__':
    GitPuller()
