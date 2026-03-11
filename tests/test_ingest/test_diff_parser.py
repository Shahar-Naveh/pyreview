"""Tests for the diff parser."""

from pyreview.ingest.diff_parser import parse_diff


SAMPLE_DIFF = """\
--- a/example.py
+++ b/example.py
@@ -1,4 +1,5 @@
 import os
+import subprocess

 def run(cmd):
-    os.system(cmd)
+    subprocess.run(cmd, shell=False, check=True)
"""


def test_parse_diff_extracts_hunks():
    hunks = parse_diff(SAMPLE_DIFF)
    assert len(hunks) == 1
    hunk = hunks[0]
    assert hunk.file_path == "example.py"
    assert len(hunk.added_lines) == 2
    assert len(hunk.removed_lines) == 1


def test_parse_diff_empty():
    hunks = parse_diff("")
    assert hunks == []
