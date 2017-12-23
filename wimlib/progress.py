from wimlib import _backend

# Progress message numbers - used to decide which progree info is valid
PROGRESS_MSG_EXTRACT_IMAGE_BEGIN = 0
PROGRESS_MSG_EXTRACT_TREE_BEGIN = 1
PROGRESS_MSG_EXTRACT_FILE_STRUCTURE = 3
PROGRESS_MSG_EXTRACT_STREAMS = 4
PROGRESS_MSG_EXTRACT_SPWM_PART_BEGIN = 5
PROGRESS_MSG_EXTRACT_METADATA = 6
PROGRESS_MSG_EXTRACT_IMAGE_END = 7
PROGRESS_MSG_EXTRACT_TREE_END = 8
PROGRESS_MSG_SCAN_BEGIN = 9
PROGRESS_MSG_SCAN_DENTRY = 10
PROGRESS_MSG_SCAN_END = 11
PROGRESS_MSG_WRITE_STREAMS = 12
PROGRESS_MSG_WRITE_METADATA_BEGIN = 13
PROGRESS_MSG_WRITE_METADATA_END = 14
PROGRESS_MSG_RENAME = 15
PROGRESS_MSG_VERIFY_INTEGRITY = 16
PROGRESS_MSG_CALC_INTEGRITY = 17
PROGRESS_MSG_SPLIT_BEGIN_PART = 19
PROGRESS_MSG_SPLIT_END_PART = 20
PROGRESS_MSG_UPDATE_BEGIN_COMMAND = 21
PROGRESS_MSG_UPDATE_END_COMMAND = 22
PROGRESS_MSG_REPLACE_FILE_IN_WIM = 23
PROGRESS_MSG_WIMBOOT_EXCLUDE = 24
PROGRESS_MSG_UNMOUNT_BEGIN = 25
PROGRESS_MSG_DONE_WITH_FILE = 26
PROGRESS_MSG_BEGIN_VERIFY_IMAGE = 27
PROGRESS_MSG_END_VERIFY_IMAGE = 28
PROGRESS_MSG_VERIFY_STREAMS = 29
# Status consts - used as returns for progress callback
PROGRESS_STATUS_CONTINUE = 0
PROGRESS_STATUS_ABORT = 1

ProgressExtract = type('ProgressExtract', (object,), {})
ProgressScan = type('ProgressScan', (object,), {})
ProgressWriteStreams = type('ProgressWriteStreams', (object,), {})
ProgressRename = type('ProgressRename', (object,), {})
ProgressUpdate = type('ProgressUpdate', (object,), {})
ProgressIntegrity = type('ProgressIntegrity', (object,), {})
ProgressSplit = type('ProgressSplit', (object,), {})
ProgressReplace = type('ProgressReplace', (object,), {})
ProgressWimbootExclude = type('ProgressWimbootExclude', (object,), {})
ProgressUnmount = type('ProgressUnmount', (object,), {})
ProgressDoneWithFile = type('ProgressDoneWithFile', (object,), {})
ProgressVerifyImage = type('ProgressVerifyImage', (object,), {})
ProgressVerifyStreams = type('ProgressVerifyStreams', (object,), {})
ProgressTestFileExclusion = type('ProgressTestFileExclusion', (object,), {})
ProgressHandleError = type('ProgressHandleError', (object,), {})
	

class WIMProgressInfo(object):
	def __init__(self):
		pass