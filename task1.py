def caching_fibonacci():
    # Створюю кеш для збереження вже знайдених чисел Фібоначчі
    cache = {}

    def fibonacci(n):
        # Якщо число 0 або менше, повертаю 0
        if n <= 0:
            return 0
        # Якщо число 1, повертаю 1
        elif n == 1:
            return 1
        # Якщо число вже є в кеші, просто повертаю його
        elif n in cache:
            return cache[n]
        
        # Обчислюю число Фібоначчі через рекурсію і зберігаю в кеші
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    
    # Повертаю внутрішню функцію, яка "пам'ятає" кеш
    return fibonacci

# Отримую функцію з кешем
fib = caching_fibonacci()

# Перевіряю, що все працює
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
