from utils.func import (
    clean_folder_and_copy_files,
    excel_process,
    WT_out,
    copy_from_downloads,
    copy2downloads
)
from UNI import uni

ACTIONS = [
    ("• Clean Folder & Copy Files", clean_folder_and_copy_files),
    ("• Open 2.1", excel_process),
    ("• WT Outbound", WT_out),
    ("• Copy 'Use' from Downloads", copy_from_downloads),
    ("• Copy 2.1 to Downloads", copy2downloads),
    ("• Uni Express", uni),
]
