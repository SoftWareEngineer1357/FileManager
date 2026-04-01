import os
import shutil
import zipfile
import tarfile
from datetime import datetime

class FileManager:
    """Простой класс файлового менеджера"""
    
    def __init__(self, config_file='config.json'):
        """Инициализация файлового менеджера"""
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.work_dir = os.path.abspath(config['working_directory'])
        self.current_dir = self.work_dir
        
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        
        print(f"Рабочая директория: {self.work_dir}")
    
    def _check_path(self, path):
        """Проверка, что путь находится в рабочей директории"""
        full_path = os.path.abspath(os.path.join(self.current_dir, path))
        if not full_path.startswith(self.work_dir):
            raise Exception("Ошибка: выход за пределы рабочей директории!")
        return full_path
    
    def ls(self, path=""):
        """Показать содержимое директории"""
        try:
            if path:
                dir_path = self._check_path(path)
            else:
                dir_path = self.current_dir
            
            if not os.path.exists(dir_path):
                return f"Путь не существует: {path}"
            
            if not os.path.isdir(dir_path):
                return f"Не является директорией: {path}"
            
            items = os.listdir(dir_path)
            if not items:
                return "Директория пуста"
            
            result = []
            result.append(f"\nСодержимое: {dir_path}")
            result.append("-" * 60)
            
            for item in sorted(items):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    result.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    result.append(f"📄 {item} ({self._format_size(size)})")
            
            result.append("-" * 60)
            result.append(f"Всего: {len(items)} элементов")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def cd(self, path):
        """Сменить директорию"""
        try:
            if path == "..":
                new_dir = os.path.dirname(self.current_dir)
            elif path == "/" or path == "~":
                new_dir = self.work_dir
            else:
                new_dir = self._check_path(path)
            
            if not os.path.exists(new_dir):
                return f"Путь не существует: {path}"
            
            if not os.path.isdir(new_dir):
                return f"Не является директорией: {path}"
            
            self.current_dir = new_dir
            return f"Текущая директория: {self.current_dir}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def pwd(self):
        """Показать текущую директорию"""
        rel_path = os.path.relpath(self.current_dir, self.work_dir)
        if rel_path == '.':
            rel_path = '/'
        return f"Текущая директория: {self.current_dir}\nОтносительно рабочей: {rel_path}"
    
    def mkdir(self, name):
        """Создать директорию"""
        try:
            dir_path = self._check_path(name)
            if os.path.exists(dir_path):
                return f"Директория уже существует: {name}"
            
            os.makedirs(dir_path)
            return f"Директория создана: {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def rmdir(self, name):
        """Удалить директорию"""
        try:
            dir_path = self._check_path(name)
            
            if not os.path.exists(dir_path):
                return f"Директория не существует: {name}"
            
            if not os.path.isdir(dir_path):
                return f"Не является директорией: {name}"
            
            if os.listdir(dir_path):
                return f"Директория не пуста. Используйте rmdir -r {name} для рекурсивного удаления"
            
            os.rmdir(dir_path)
            return f"Директория удалена: {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def rmdir_recursive(self, name):
        """Рекурсивно удалить директорию"""
        try:
            dir_path = self._check_path(name)
            
            if not os.path.exists(dir_path):
                return f"Директория не существует: {name}"
            
            shutil.rmtree(dir_path)
            return f"Директория удалена (рекурсивно): {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def touch(self, name, content=""):
        """Создать файл"""
        try:
            file_path = self._check_path(name)
            
            if os.path.exists(file_path):
                return f"Файл уже существует: {name}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Файл создан: {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def cat(self, name):
        """Показать содержимое файла"""
        try:
            file_path = self._check_path(name)
            
            if not os.path.exists(file_path):
                return f"Файл не существует: {name}"
            
            if not os.path.isfile(file_path):
                return f"Не является файлом: {name}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content:
                return "Файл пуст"
            
            return content
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def write(self, name, content, append=False):
        """Записать в файл"""
        try:
            file_path = self._check_path(name)
            
            if not os.path.exists(file_path):
                return f"Файл не существует: {name}"
            
            mode = 'a' if append else 'w'
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return f"Файл {'дополнен' if append else 'перезаписан'}: {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def rm(self, name):
        """Удалить файл"""
        try:
            file_path = self._check_path(name)
            
            if not os.path.exists(file_path):
                return f"Файл не существует: {name}"
            
            if not os.path.isfile(file_path):
                return f"Не является файлом: {name}"
            
            os.remove(file_path)
            return f"Файл удален: {name}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def cp(self, source, dest):
        """Скопировать файл"""
        try:
            src_path = self._check_path(source)
            dst_path = self._check_path(dest)
            
            if not os.path.exists(src_path):
                return f"Исходный файл не существует: {source}"
            
            if not os.path.isfile(src_path):
                return f"Не является файлом: {source}"
            
            if os.path.exists(dst_path):
                return f"Файл назначения уже существует: {dest}"
            
            shutil.copy2(src_path, dst_path)
            return f"Файл скопирован: {source} -> {dest}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def mv(self, source, dest):
        """Переместить или переименовать файл"""
        try:
            src_path = self._check_path(source)
            dst_path = self._check_path(dest)
            
            if not os.path.exists(src_path):
                return f"Исходный файл не существует: {source}"
            
            if os.path.exists(dst_path):
                return f"Файл назначения уже существует: {dest}"
            
            shutil.move(src_path, dst_path)
            return f"Файл перемещен/переименован: {source} -> {dest}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def info(self, name):
        """Информация о файле или директории"""
        try:
            path = self._check_path(name)
            
            if not os.path.exists(path):
                return f"Путь не существует: {name}"
            
            stat = os.stat(path)
            
            info = []
            info.append(f"\nИнформация о: {name}")
            info.append("-" * 40)
            info.append(f"Тип: {'Директория' if os.path.isdir(path) else 'Файл'}")
            info.append(f"Размер: {self._format_size(stat.st_size)}")
            info.append(f"Создан: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"Изменен: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def search(self, pattern):
        """Поиск файлов по имени"""
        try:
            results = []
            for root, dirs, files in os.walk(self.current_dir):
                # Проверяем, что не выходим за пределы рабочей директории
                if not root.startswith(self.work_dir):
                    continue
                
                for item in files + dirs:
                    if pattern.lower() in item.lower():
                        rel_path = os.path.relpath(os.path.join(root, item), self.work_dir)
                        results.append(rel_path)
            
            if not results:
                return f"Файлы/папки с '{pattern}' не найдены"
            
            result_text = [f"\nНайдено {len(results)} элементов:"]
            for item in results:
                result_text.append(f"  • {item}")
            
            return "\n".join(result_text)
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def archive(self, name, items):
        """Создать ZIP архив"""
        try:
            # Создаем путь к архиву
            archive_path = self._check_path(name)
            if not archive_path.endswith('.zip'):
                archive_path += '.zip'
            
            # Проверяем, не существует ли архив
            if os.path.exists(archive_path):
                return f"Архив уже существует: {name}"
            
            # Создаем архив
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item in items:
                    item_path = self._check_path(item)
                    if not os.path.exists(item_path):
                        return f"Элемент не существует: {item}"
                    
                    # Добавляем в архив
                    if os.path.isfile(item_path):
                        zipf.write(item_path, os.path.basename(item_path))
                    else:
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, os.path.dirname(item_path))
                                zipf.write(file_path, arcname)
            
            return f"Архив создан: {os.path.basename(archive_path)}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def extract(self, archive_name, extract_to=""):
        """Распаковать ZIP архив"""
        try:
            archive_path = self._check_path(archive_name)
            
            if not os.path.exists(archive_path):
                return f"Архив не найден: {archive_name}"
            
            if not archive_path.endswith('.zip'):
                return f"Поддерживаются только ZIP архивы"
            
            # Определяем куда распаковывать
            if extract_to:
                extract_path = self._check_path(extract_to)
                if not os.path.exists(extract_path):
                    os.makedirs(extract_path)
            else:
                extract_path = self.current_dir
            
            # Распаковываем
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_path)
            
            return f"Архив распакован в: {extract_path}"
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def tree(self):
        """Показать дерево директорий"""
        try:
            result = []
            self._print_tree(self.current_dir, "", result)
            return "\n".join(result)
            
        except Exception as e:
            return f"Ошибка: {e}"
    
    def _print_tree(self, path, prefix, result):
        """Рекурсивно выводит дерево директорий"""
        items = sorted(os.listdir(path))
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = i == len(items) - 1
            
            if os.path.isdir(item_path):
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._print_tree(item_path, new_prefix, result)
            else:
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{item}")
    
    def _format_size(self, size):
        """Форматирование размера файла"""
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} ТБ"
    
    def help(self):
        """Показать справку"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    ПРОСТОЙ ФАЙЛОВЫЙ МЕНЕДЖЕР                 ║
╠══════════════════════════════════════════════════════════════╣
║ КОМАНДЫ:                                                     ║
║                                                              ║
║   help          - показать эту справку                       ║
║   exit / quit   - выйти из программы                         ║
║                                                              ║
║   ls [путь]     - показать содержимое директории             ║
║   cd <путь>     - перейти в директорию                       ║
║   pwd           - показать текущую директорию                ║
║   mkdir <имя>   - создать директорию                         ║
║   rmdir <имя>   - удалить пустую директорию                  ║
║   rmdir -r <имя>- удалить директорию со всем содержимым      ║
║   tree          - показать дерево директорий                 ║
║                                                              ║
║   touch <имя>   - создать пустой файл                        ║
║   cat <имя>     - показать содержимое файла                  ║
║   write <имя>   - записать текст в файл                      ║
║   write -a <имя>- добавить текст в конец файла               ║
║   rm <имя>      - удалить файл                               ║
║   cp <src> <dst>- скопировать файл                           ║
║   mv <src> <dst>- переместить или переименовать файл         ║
║   info <имя>    - информация о файле/папке                   ║
║   search <текст>- поиск файлов и папок по имени              ║
║                                                              ║
║   archive <имя> <файлы...> - создать ZIP архив               ║
║   extract <архив> [путь]   - распаковать ZIP архив           ║
╚══════════════════════════════════════════════════════════════╝
        """
        return help_text


def main():
    """Основная функция"""
    print("Загрузка файлового менеджера...")
    
    # Создаем экземпляр менеджера
    fm = FileManager()
    
    print("\nФайловый менеджер запущен!")
    print("Введите 'help' для списка команд\n")
    
    # Основной цикл
    while True:
        try:
            # Получаем текущую директорию для приглашения
            rel_path = os.path.relpath(fm.current_dir, fm.work_dir)
            if rel_path == '.':
                rel_path = '/'
            
            # Ввод команды
            command = input(f"\n{rel_path}> ").strip()
            
            if not command:
                continue
            
            # Разбираем команду
            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:]
            
            # Выполняем команду
            if cmd == 'exit' or cmd == 'quit':
                print("До свидания!")
                break
            
            elif cmd == 'help':
                print(fm.help())
            
            elif cmd == 'ls':
                path = args[0] if args else ""
                print(fm.ls(path))
            
            elif cmd == 'cd':
                if not args:
                    print("Использование: cd <путь>")
                else:
                    print(fm.cd(args[0]))
            
            elif cmd == 'pwd':
                print(fm.pwd())
            
            elif cmd == 'mkdir':
                if not args:
                    print("Использование: mkdir <имя>")
                else:
                    print(fm.mkdir(args[0]))
            
            elif cmd == 'rmdir':
                if not args:
                    print("Использование: rmdir <имя> или rmdir -r <имя>")
                elif args[0] == '-r':
                    if len(args) < 2:
                        print("Использование: rmdir -r <имя>")
                    else:
                        print(fm.rmdir_recursive(args[1]))
                else:
                    print(fm.rmdir(args[0]))
            
            elif cmd == 'touch':
                if not args:
                    print("Использование: touch <имя_файла>")
                else:
                    content = ' '.join(args[1:]) if len(args) > 1 else ""
                    print(fm.touch(args[0], content))
            
            elif cmd == 'cat':
                if not args:
                    print("Использование: cat <имя_файла>")
                else:
                    print(fm.cat(args[0]))
            
            elif cmd == 'write':
                if not args:
                    print("Использование: write <имя_файла> [текст] или write -a <имя_файла> [текст]")
                elif args[0] == '-a':
                    if len(args) < 2:
                        print("Использование: write -a <имя_файла> [текст]")
                    else:
                        content = ' '.join(args[2:]) if len(args) > 2 else input("Введите текст для добавления: ")
                        print(fm.write(args[1], content, append=True))
                else:
                    content = ' '.join(args[1:]) if len(args) > 1 else input("Введите текст для записи: ")
                    print(fm.write(args[0], content))
            
            elif cmd == 'rm':
                if not args:
                    print("Использование: rm <имя_файла>")
                else:
                    print(fm.rm(args[0]))
            
            elif cmd == 'cp':
                if len(args) < 2:
                    print("Использование: cp <источник> <назначение>")
                else:
                    print(fm.cp(args[0], args[1]))
            
            elif cmd == 'mv':
                if len(args) < 2:
                    print("Использование: mv <источник> <назначение>")
                else:
                    print(fm.mv(args[0], args[1]))
            
            elif cmd == 'info':
                if not args:
                    print("Использование: info <имя>")
                else:
                    print(fm.info(args[0]))
            
            elif cmd == 'search':
                if not args:
                    print("Использование: search <текст>")
                else:
                    print(fm.search(' '.join(args)))
            
            elif cmd == 'archive':
                if len(args) < 2:
                    print("Использование: archive <имя_архива> <файл1> [файл2 ...]")
                else:
                    print(fm.archive(args[0], args[1:]))
            
            elif cmd == 'extract':
                if not args:
                    print("Использование: extract <архив> [путь_для_распаковки]")
                else:
                    extract_to = args[1] if len(args) > 1 else ""
                    print(fm.extract(args[0], extract_to))
            
            elif cmd == 'tree':
                print(fm.tree())
            
            else:
                print(f"Неизвестная команда: {cmd}. Введите 'help' для списка команд.")
        
        except KeyboardInterrupt:
            print("\n\nДля выхода используйте команду 'exit'")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()