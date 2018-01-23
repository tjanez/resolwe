"""Global settings for Flow executor."""
import json

from .protocol import ExecutorFiles  # pylint: disable=import-error

DESERIALIZED_FILES = {}  # pylint: disable=invalid-name
with open(ExecutorFiles.EXECUTOR_SETTINGS, 'rt') as _settings_file:
    DESERIALIZED_FILES[ExecutorFiles.EXECUTOR_SETTINGS] = json.load(_settings_file)
    for _file_name in DESERIALIZED_FILES[ExecutorFiles.EXECUTOR_SETTINGS][ExecutorFiles.FILE_LIST_KEY]:
        with open(_file_name, 'rt') as _json_file:
            DESERIALIZED_FILES[_file_name] = json.load(_json_file)

EXECUTOR_SETTINGS = DESERIALIZED_FILES[ExecutorFiles.EXECUTOR_SETTINGS]
SETTINGS = DESERIALIZED_FILES[ExecutorFiles.DJANGO_SETTINGS]
DATA = DESERIALIZED_FILES[ExecutorFiles.DATA]
DATA_META = DESERIALIZED_FILES[ExecutorFiles.DATA_META]
PROCESS = DESERIALIZED_FILES[ExecutorFiles.PROCESS]
PROCESS_META = DESERIALIZED_FILES[ExecutorFiles.PROCESS_META]
