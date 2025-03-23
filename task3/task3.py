import sys
from collections import Counter

# Ось тут починається магія парсингу логів. Я розділяю рядок на частини: дата, час, рівень і повідомлення.
def parse_log_line(line: str) -> dict:
    """
    Парсинг одного рядка логів у його складові.
    Приклад рядка: 2024-01-22 08:30:01 INFO Користувач увійшов успішно.
    """
    try:
        parts = line.split(" ", 3)  # Я ріжу рядок по пробілах, намагаючись отримати 4 частини.
        if len(parts) < 4:  # Якщо частин менше 4, значить щось пішло не так.
            return None
        
        date, time, level, message = parts  # Розпаковую ці частини у змінні.
        return {
            "date": date,  # Дата буде тут.
            "time": time,  # Час буде тут.
            "level": level,  # Рівень логування (INFO, ERROR тощо).
            "message": message.strip()  # Повідомлення, без зайвих пробілів.
        }
    except Exception:
        return None  # Якщо щось пішло не так, повертаю None, бо парсити не вдалося.

# Тепер я загружаю логи з файлу і парсю кожен рядок. Ось де я намагаюся бути дуже ефективним.
def load_logs(file_path: str) -> list:
    """
    Завантажуємо логи з файлу та парсимо кожен рядок.
    """
    logs = []  # Тут я буду зберігати всі гарно розібрані логи.
    try:
        with open(file_path, 'r') as file:  # Відкриваю файл на читання.
            for line in file:  # Прочитав кожен рядок і одразу його парсю.
                parsed_line = parse_log_line(line)  # Парсинг цього рядка.
                if parsed_line:  # Якщо парсинг вдалий, додаю до списку логів.
                    logs.append(parsed_line)
        return logs  # Повертаю список всіх гарно оброблених логів.
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")  # Якщо файл не знайдений, лякаю користувача.
        sys.exit(1)  # Виходжу з помилкою.
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")  # Якщо інша помилка, також виходжу з помилкою.
        sys.exit(1)

# Тут я фільтрую логи за рівнем, наприклад, тільки "INFO" або "ERROR".
def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрую логи за певним рівнем.
    """
    return [log for log in logs if log["level"].upper() == level.upper()]  # Збираю всі логи, де рівень збігається.

# І ось я рахую, скільки логів кожного рівня.
def count_logs_by_level(logs: list) -> dict:
    """
    Рахую логи за рівнями.
    """
    level_counts = Counter(log["level"] for log in logs)  # Використовую Counter для лічильника рівнів.
    return dict(level_counts)  # Повертаю це як звичайний словник.

# Тепер буду красиво виводити на екран статистику по кількості логів кожного рівня.
def display_log_counts(counts: dict):
    """
    Вивожу кількість логів по рівнях у вигляді таблиці.
    """
    print("Рівень логування | Кількість")  # Шапка таблиці.
    print("-----------------|----------")  # Лінія для розмежування.
    for level, count in counts.items():  # Для кожного рівня і його кількості виводимо.
        print(f"{level:<16} | {count}")  # Форматую виведення красиво.

# Якщо мені треба вивести всі логи для певного рівня, то ось це моя функція.
def display_logs_by_level(logs: list, level: str):
    """
    Вивожу всі логи певного рівня.
    """
    filtered_logs = filter_logs_by_level(logs, level)  # Спочатку фільтрую логи за рівнем.
    
    if not filtered_logs:  # Якщо логи відсутні, повідомляю про це.
        print(f"No logs found for level '{level}'.")  # Вивожу повідомлення, що логи не знайдені.
        return
    
    print(f"\nДеталі логів для рівня '{level}':")  # Заголовок для виведення.
    for log in filtered_logs:  # Для кожного логу виводимо його деталі.
        print(f"{log['date']} {log['time']} - {log['message']}")  # Виводжу дату, час і повідомлення.

def main():
    # Перевіряю, чи достатньо аргументів передано (файл і опціонально рівень).
    if len(sys.argv) < 2:
        print("Usage: python task3.py <log_file_path> [log_level]")  # Якщо аргументів мало, показую, як запускати.
        sys.exit(1)  # Виходжу з помилкою.

    log_file_path = sys.argv[1]  # Перший аргумент — це шлях до файлу.

    # Загружаю логи з файлу.
    logs = load_logs(log_file_path)
    
    # Рахую кількість логів за рівнями.
    level_counts = count_logs_by_level(logs)
    
    # Виводжу статистику по кількості логів.
    display_log_counts(level_counts)
    
    # Якщо вказано рівень, виводжу логи для цього рівня.
    if len(sys.argv) > 2:
        level = sys.argv[2]  # Другий аргумент — це рівень логів.
        display_logs_by_level(logs, level)

# Тут все починається. Якщо файл запускається як головний, запускаю main().
if __name__ == "__main__":
    main()
