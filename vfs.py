import zipfile
import os

class VFS:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_file = zipfile.ZipFile(zip_path, 'a')  # Открытие архива в режиме добавления
        self.current_path = '/'

    def list_dir(self, path):
        try:
            all_files = self.zip_file.namelist()  # Получаем список всех файлов в архиве
            normalized_path = path.lstrip('/')  # Убираем начальный "/"

            if normalized_path and not normalized_path.endswith('/'):
                normalized_path += '/'  # Убедимся, что путь заканчивается "/"

            contents = set()
            for file in all_files:
                if file.startswith(normalized_path):  # Проверяем, лежит ли файл в каталоге
                    relative_path = file[len(normalized_path):].lstrip('/').split('/')[0]
                    if relative_path:
                        contents.add(relative_path)  # Добавляем уникальные файлы/папки в результат

            return sorted(contents)
        except Exception as e:
            raise Exception(f"Error reading directory '{path}': {str(e)}")

    def list_files(self, path):
        return [file for file in self.zip_file.namelist() if file.startswith(path)]

    def read_file(self, path):
        try:
            with self.zip_file.open(path) as f:
                return f.read().decode('utf-8')
        except KeyError:
            raise KeyError(f"There is no file named '{path}' in the archive")
        except Exception as e:
            raise Exception(f"Error reading file '{path}': {str(e)}")

    def directory_exists(self, path):
        normalized_path = path.lstrip('/')
        if not normalized_path.endswith('/'):
            normalized_path += '/'
        return any(file.startswith(normalized_path) for file in self.zip_file.namelist())

    def close(self):
        self.zip_file.close()

    def remove_file(self, path):
        """Удаление файла из виртуальной файловой системы (архива)."""
        if path not in self.zip_file.namelist():
            raise FileNotFoundError(f"File '{path}' not found in VFS.")

        # Создаем новый временный архив без удаляемого файла
        temp_zip_path = self.zip_path + '.temp'
        with zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
            for file_name in self.zip_file.namelist():
                if file_name != path:
                    temp_zip.writestr(file_name, self.zip_file.read(file_name))

        # Удаляем оригинальный архив и переименовываем временный
        os.remove(self.zip_path)
        os.rename(temp_zip_path, self.zip_path)

    def create_file(self, path):
        """Создание нового пустого файла в архиве (аналог команды touch)."""
        # Если файл уже существует, ничего не делаем
        if path in self.zip_file.namelist():
            return

        # Добавляем пустой файл в архив
        with self.zip_file.open(path, 'w') as f:
            pass  # Пишем пустое содержимое
