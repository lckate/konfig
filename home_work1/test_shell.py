import unittest
from shell import Shell
from vfs import VFS

class TestShell(unittest.TestCase):
    def setUp(self):
        # Инициализация конфигурации
        config = {
            'user': 'user1',
            'host': 'localhost',
            'vfs_path': 'test.zip'  # Путь к архиву виртуальной файловой системы
        }
        self.shell = Shell(config)

    def test_ls(self):
        # Test ls in root directory
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('test', result)  # Пример файлов в корне
        self.assertIn('test2', result)
        self.assertIn('test3', result)

        # Test ls in a specific directory
        self.shell.cd('test')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('bbb.txt', result)

        self.shell.cd('..')
        self.shell.cd('test2')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('eee.txt', result)
        self.assertIn('qqq.txt', result)

        self.shell.cd('..')
        self.shell.cd('test3')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('ddd.txt', result)
        self.assertIn('fff.txt', result)

    def test_cd(self):
        # Test cd to existing directory
        result = self.shell.cd('test')
        self.assertIn('Changed directory to', result)

        # Test cd to non-existing directory
        result = self.shell.cd('non_existing_directory')
        self.assertIn('cd: no such directory', result)

        # Test cd to parent directory
        self.shell.cd('test')
        result = self.shell.cd('..')
        self.assertIn('Changed directory to', result)

    def test_rm(self):
        # Test rm on existing file
        self.shell.cd('test')
        result = self.shell.rm('bbb.txt')
        self.assertIn('File bbb.txt removed.', result)

        # Test rm on non-existing file
        result = self.shell.rm('non_existing_file.txt')
        self.assertIn('rm: no such file or directory', result)

    def test_touch(self):
        # Test touch for creating a new file
        result = self.shell.touch('newfile.txt')
        self.assertIn('File newfile.txt created.', result)

        # Test touch for an existing file
        result = self.shell.touch('newfile.txt')
        self.assertIn('touch: file already exists', result)

    def test_exit(self):
        # Test exit command
        result = self.shell.exit()
        self.assertEqual(result, "Exiting shell...")

if __name__ == '__main__':
    unittest.main()
