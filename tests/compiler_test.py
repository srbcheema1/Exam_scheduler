import pytest
import os

from srblib import verify_folder, verify_file, remove, file_name, file_extension, abs_path, on_ci
from exam_scheduler.verifier import Compiler

def test_room_compiler():
    if not on_ci:
        return
    ans = Compiler.verify_room_list('.ci/room_list.xlsx')
    assert(ans == True)
