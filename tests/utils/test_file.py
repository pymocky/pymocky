import os
import unittest

from app.utils.file import File


class FileTests(unittest.TestCase):
    def test_get_yaml_files(self):
        files = File.get_yaml_files(os.path.join(os.getcwd(), "extras", "sample"))
        files = list(files)
        total = len(files)

        self.assertEqual(total, 7)

    def test_real_path(self):
        base_path = ""
        file_path = os.path.join("extras", "sample", "files", "dummy.pdf")
        path = File.real_path(base_path, "//{0}".format(file_path))
        real_path = os.path.join(os.getcwd(), file_path)

        self.assertEqual(real_path, path)

    def test_real_path_with_base_path(self):
        base_path = "/my-base-path"
        file_path = os.path.join("extras", "sample", "files", "dummy.pdf")
        path = File.real_path(base_path, "//{0}".format(file_path))
        real_path = os.path.abspath("/my-base-path/extras/sample/files/dummy.pdf")

        self.assertEqual(real_path, path)

    def test_real_path_with_base_path_but_ignore(self):
        base_path = "my-base-path"
        file_path = os.path.join("extras", "sample", "files", "dummy.pdf")
        path = File.real_path(base_path, "/{0}".format(file_path))
        real_path = os.path.abspath("/extras/sample/files/dummy.pdf")

        self.assertEqual(real_path, path)

    def test_create_dir(self):
        path = os.path.join(os.getcwd(), "temp")

        File.remove_dir(path)
        File.create_dir(path)

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_remove_dir(self):
        path = os.path.join(os.getcwd(), "temp")

        File.remove_dir(path)
        File.create_dir(path)
        File.remove_dir(path)

        exists = os.path.exists(path)

        self.assertFalse(exists)
