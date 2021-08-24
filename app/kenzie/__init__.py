from environs import Env
import os

env = Env()
env.read_env()

main_dir = env('FILES_DIRECTORY')

directories = ('', 'gif', 'jpg', 'png')

for extension in directories:
    directory = os.path.join(main_dir, extension)
    if not os.path.exists(directory):
        os.makedirs(directory)