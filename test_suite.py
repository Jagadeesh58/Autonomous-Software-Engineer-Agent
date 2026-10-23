"""
test_suite.py - Unit tests for Autonomous Software Engineer Agent tools and core functions.
"""

import os
import unittest
from tools import (
    run_shell,
    read_file,
    write_file,
    append_file,
    list_directory,
    execute_code,
    TOOL_MAP,
    TOOL_SCHEMAS
)
from agent import normalize_tool_args, trim_history_for_context


class TestTools(unittest.TestCase):
    def setUp(self):
        self.test_file = "_test_sample.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_tool_map_and_schemas_match(self):
        schema_names = {s["function"]["name"] for s in TOOL_SCHEMAS}
        map_names = set(TOOL_MAP.keys())
        self.assertEqual(schema_names, map_names, "TOOL_MAP and TOOL_SCHEMAS tool names must match exactly!")

    def test_write_read_and_append_file(self):
        # Write
        res_write = write_file(self.test_file, "Line 1\n")
        self.assertIn("File written", res_write)
        self.assertTrue(os.path.exists(self.test_file))

        # Append
        res_append = append_file(self.test_file, "Line 2\n")
        self.assertIn("Content appended", res_append)

        # Read
        content = read_file(self.test_file)
        self.assertEqual(content, "Line 1\nLine 2\n")

    def test_read_file_not_found(self):
        res = read_file("non_existent_file_xyz_123.txt")
        self.assertTrue(res.startswith("Error: File not found"))

    def test_run_shell(self):
        res = run_shell("echo hello_world")
        self.assertIn("hello_world", res)

    def test_list_directory(self):
        res = list_directory(".")
        self.assertIn("Contents of", res)
        self.assertIn("tools.py", res)

    def test_execute_code(self):
        res = execute_code("print(123 + 456)")
        self.assertEqual(res.strip(), "579")

    def test_execute_code_error(self):
        res = execute_code("raise ValueError('something went wrong')")
        self.assertIn("ValueError", res)


class TestAgentHelpers(unittest.TestCase):
    def test_normalize_tool_args(self):
        # Code arg
        args1 = normalize_tool_args("execute_code", {"input": "print('hi')"})
        self.assertEqual(args1, {"code": "print('hi')"})

        # File path arg
        args2 = normalize_tool_args("read_file", {"file_name": "test.py"})
        self.assertEqual(args2, {"path": "test.py"})

        # Command arg
        args3 = normalize_tool_args("run_shell", {"cmd": "dir"})
        self.assertEqual(args3, {"command": "dir"})

        # Search query arg
        args4 = normalize_tool_args("do_search", {"search_query": "python"})
        self.assertEqual(args4, {"query": "python"})

    def test_trim_history_for_context(self):
        msgs = [{"role": "user", "content": "Initial task"}]
        for i in range(20):
            msgs.append({"role": "tool", "content": "x" * 2000, "name": "run_shell"})

        trimmed = trim_history_for_context(msgs)
        self.assertEqual(trimmed[0]["content"], "Initial task")
        # Older tool message should be truncated
        self.assertIn("[output truncated for context limit]", trimmed[1]["content"])


if __name__ == "__main__":
    unittest.main()
