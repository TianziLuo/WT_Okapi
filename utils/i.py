import os
import glob
from send2trash import send2trash  

def clean_folder():
    folder_path = r'C:\Frank\易仓-TP\无小票发货 Sarah'

    # Get all .xlsx and .csv files 
    file_patterns = ['*.xlsx', '*.csv']
    files_to_delete = []

    for pattern in file_patterns:
        files_to_delete.extend(glob.glob(os.path.join(folder_path, pattern)))

    # Move each file to Recycle Bin
    for file in files_to_delete:
        try:
            send2trash(file)  # trash bin
            print(f"Moved to Recycle Bin: {file}")
        except Exception as e:
            print(f"Failed to move: {file}, Reason: {e}")

    # Open the folder in File Explorer
    os.startfile(folder_path)

'''
if __name__ == "__main__":
    clean_folder()
'''