import datetime
import os
import subprocess
from vfs import VFS

class Shell:
    def __init__(self, config):
        # Инициализация с конфигурацией и виртуальной файловой системой
        self.config = config
        self.vfs = VFS(config['vfs_path'])  # VFS инициализируется с путем к виртуальной файловой системе
        self.current_path = '/'  # Стартовая директория

    def execute(self, command):
        # Основной метод для выполнения команд
        parts = command.strip().split()
        if not parts:
            return ''  # Пустая команда, ничего не делаем

        cmd = parts[0]
        args = parts[1:]

        # Обработка команд
        if cmd == 'ls':
            return self.ls()
        elif cmd == 'cd':
            return self.cd(args[0]) if args else 'cd: missing argument'
        elif cmd == 'exit':
            return self.exit()
        elif cmd == 'rm':
            return self.rm(args[0]) if args else 'rm: missing argument'
        elif cmd == 'touch':
            return self.touch(args[0]) if args else 'touch: missing argument'
        else:
            return f"Unknown command: {cmd}"

    def ls(self):
        """Команда ls: выводит содержимое текущей директории"""
        try:
            contents = self.vfs.list_dir(self.current_path)  # Используем метод list_dir из VFS
            if contents:
                return '\n'.join(contents)
            return 'Empty directory'
        except Exception as e:
            return f"ls: error listing directory: {str(e)}"

    def cd(self, path):
        """Команда cd: изменяет текущую директорию"""
        try:
            if path == '..':  # Переход на уровень выше
                new_path = os.path.dirname(self.current_path.rstrip('/'))
                self.current_path = new_path if new_path else '/'
            else:
                new_path = os.path.join(self.current_path, path).replace('\\', '/')
                if self.vfs.directory_exists(new_path):  # Проверяем, существует ли директория
                    self.current_path = new_path
                else:
                    return f"cd: no such directory: {path}"
            return f"Changed directory to {self.current_path}"
        except Exception as e:
            return f"cd: error changing directory: {str(e)}"

    def exit(self):
        """Команда exit: завершает работу оболочки"""
        self.vfs.close()  # Закрываем виртуальную файловую систему, если требуется
        return "Exiting shell..."

    def rm(self, filename):
        """Команда rm: удаляет файл из виртуальной файловой системы"""
        try:
            self.vfs.remove_file(os.path.join(self.current_path, filename))  # Удаляем файл
            return f"File {filename} removed."
        except FileNotFoundError:
            return f"rm: no such file or directory: {filename}"
        except Exception as e:
            return f"rm: error removing file: {str(e)}"

    def touch(self, filename):
        """Команда touch: создает новый пустой файл в текущей директории"""
        try:
            self.vfs.create_file(os.path.join(self.current_path, filename))  # Создаем файл
            return f"File {filename} created."
        except FileExistsError:
            return f"touch: file already exists: {filename}"
        except Exception as e:
            return f"touch: error creating file: {str(e)}"


