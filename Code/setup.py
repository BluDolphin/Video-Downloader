import shutil
import os

# Specify the source folder path
current_path = os.getcwd()
source_folder = '\_internal\\ffmpegio'
#combine the current path with the source folder
source_folder = current_path + source_folder

# Get the path to the local app data directory
local_app_data_dir = os.environ.get('LOCALAPPDATA')

print("WINDOWS ONLY, OTHER OS WILL NEED TO INSTALL FFMPEG MANUALLY")
input("This program will automatically move the required ffmpeg files to the AppData folder. Press Enter to continue.")

if local_app_data_dir:
    # Construct the destination folder path within AppData\Local
    destination_folder = os.path.join(local_app_data_dir, 'ffmpegio')

    try:
        if os.path.exists(source_folder):
            if not os.path.exists(destination_folder):
                shutil.move(source_folder, destination_folder)
                print(f'Folder moved from {source_folder} to {destination_folder}')
            else:
                print(f'Destination folder already exists: {destination_folder}')
        else:
            print(f'Source folder does not exist: {source_folder}')
    except shutil.Error as e:
        print(f'Error occurred while moving folder: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
else:
    print('Could not get the path to Local AppData directory.')