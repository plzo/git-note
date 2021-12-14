import os
import sys


root_dir = 'C:/Users'
def remove_dumps():
    for one_user in os.listdir(root_dir):
        CrashDumps_path = root_dir + '/' + one_user + '/AppData/Local/CrashDumps'
        if os.path.exists(CrashDumps_path):
            for one_dump in os.listdir(CrashDumps_path):
                if one_dump.endswith('.dmp'):
                    os.remove(CrashDumps_path + '/' + one_dump)
                    print('delete dmp :', CrashDumps_path + '/' + one_dump)

if __name__ == '__main__':
    remove_dumps()





