from utils.func import (
    excel_process,
    WT_out,
    copy_from_downloads,
    copy2downloads
)

ACTIONS = [
    ("• Open 2.1", excel_process),
    ("• WT Outbound", WT_out),
    ("• Copy 'Use' from Downloads", copy_from_downloads),
    ("• Copy 2.1 to Downloads", copy2downloads),
]
