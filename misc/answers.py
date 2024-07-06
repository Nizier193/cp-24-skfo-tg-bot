from config import Config

assistant_entry = """
Здравствуйте!

Я - умный ассистент RuStore, который поможет вам разрешить любую проблему,
связанную с документацией или кодом!

Не стесняйтесь обращаться по любому вопросу или загружать свои файлы,
чтобы я мог лучше помочь вам с проблемой.

Основной сайт с документацией:
https://www.rustore.ru/help/
"""

assistant_help = """
Что может этот бот? - Помощь по командам.
Бот натренирован отвечать в соответствии с документацией RuStore.

**Поможет вам в сложной ситуации с кодом:**
1. Напишите боту любой текст (в том числе и с кодом) и он поможет вам разрешить проблему!

**Проанализирует поданные ему файлы**
2. /upload_file
После запуска команды отправьте боту файл и он поможет вам с чем-либо, используя информацию!

**Поможет написать что угодно!**
3. Используйте его как помощника, он настроен помогать вам с любыми проблемами RuStore.
"""

assistant_query = """
Вижу вы готовы задавать вопросы!
Напишите, что именно вам непонятно и я вам помогу.

* Для разрешения вопросов, связанных с кодом, вы можете заключать код в тройные "`"
"""

assistant_files = """
Вижу, вы хотите добавить свой файл для анализа!

Учтите, что при использовании другими пользователями этого бота, нейросеть будет
выдавать результаты с использованием знаний загруженного файла.

Приступим! Отправьте нужный вам файл и я его проанализирую.
"""

assistant_files_success = """
Вы успешно загрузили файл!
Скоро его изучу и помогу вам с разрешением любых проблем!
"""

configuration = "\n".join([f'{name[:12]}.. - {str(value)[:12]}..' for name, value in Config.__dict__.items()])
assistant_config = f"""
Загруженная конфигурация бота:
{configuration}
Для изменений необходимо использовать config.Config и config.Providers
"""