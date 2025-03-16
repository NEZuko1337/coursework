import pandas as pd


def load_data_from_excel(file_path):
    """
    Загружает данные из Excel файла.

    Args:
        file_path (str): Путь к Excel файлу с данными

    Returns:
        tuple: (investments, profits) где:
            - investments: список возможных сумм инвестиций
            - profits: матрица прибылей для каждого предприятия
    """
    df = pd.read_excel(file_path, header=None)
    profit_table = df.values.tolist()

    # Извлечём список возможных инвестиций и матрицу прибылей
    investments = [row[0] for row in profit_table]
    profits = [row[1:] for row in profit_table]  # убираем первый столбец с числом инвестиций

    return investments, profits


def load_data_from_array(data_array):
    """
    Загружает данные из двумерного массива.

    Args:
        data_array (list): Двумерный массив данных (как profit_table)

    Returns:
        tuple: (investments, profits) где:
            - investments: список возможных сумм инвестиций
            - profits: матрица прибылей для каждого предприятия
    """
    # Извлечём список возможных инвестиций и матрицу прибылей
    investments = [row[0] for row in data_array]
    profits = [row[1:] for row in data_array]  # убираем первый столбец с числом инвестиций

    return investments, profits


def get_profit(profits, investments, e, x):
    """
    Получает прибыль, если вложить x млн в e-е предприятие.

    Args:
        profits (list): Матрица прибылей
        investments (list): Список возможных сумм инвестиций
        e (int): Индекс предприятия (0..num_enterprises-1)
        x (int): Сумма инвестиций (например, 10, 20, 30...)

    Returns:
        float: Прибыль от инвестиции x в предприятие e
    """
    # Находим индекс i, где investments[i] == x
    i = investments.index(x)
    return profits[i][e]


def optimize_investments(investments, profits):
    """
    Оптимизирует распределение инвестиций между предприятиями с использованием
    динамического программирования.

    Args:
        investments (list): Список возможных сумм инвестиций
        profits (list): Матрица прибылей для каждого предприятия

    Returns:
        tuple: (max_profit, distribution) где:
            - max_profit: максимальная суммарная прибыль
            - distribution: список распределения инвестиций по предприятиям
    """
    # Сколько всего предприятий и уровней инвестиций
    num_enterprises = len(profits[0])
    num_invest_levels = len(investments)

    # Инициализация матриц DP и выбора
    dp = [[0] * (num_invest_levels) for _ in range(num_enterprises + 1)]
    choice = [[0] * (num_invest_levels) for _ in range(num_enterprises + 1)]

    # Заполняем DP
    for i in range(1, num_enterprises + 1):
        # i - количество предприятий, которые учитываем (1..num_enterprises)
        for j in range(num_invest_levels):
            # j - индекс возможного уровня инвестиций (0..num_invest_levels-1)
            best_profit = 0
            best_k = 0

            # Перебираем, сколько вложить в текущее предприятие i-1 (по индексу e = i-1)
            for k in range(j + 1):
                # k пробегает от 0 до j, это индекс уровня инвестиций в предприятие i-1
                invest_in_this = investments[k]  # например, 0,10,20,...
                # Остаток уходит на i-1 предприятий, и это dp[i-1][j-k]
                current_profit = dp[i-1][j-k] + get_profit(profits, investments, i-1, invest_in_this)
                if current_profit > best_profit:
                    best_profit = current_profit
                    best_k = k
            dp[i][j] = best_profit
            choice[i][j] = best_k  # запоминаем, сколько вложили в i-ое (точнее индекс k)

    # Максимальная прибыль
    max_profit = dp[num_enterprises][num_invest_levels - 1]

    # Восстановление решения
    distribution = [0] * num_enterprises
    remaining_j = num_invest_levels - 1  # начинаем с последнего уровня инвестиций
    for i in range(num_enterprises, 0, -1):
        # Смотрим, сколько вложили в i-е предприятие (индекс i-1)
        k = choice[i][remaining_j]  # индекс уровня инвестиций в i-е предприятие
        invest_in_this = investments[k]
        distribution[i - 1] = invest_in_this
        # Оставшийся бюджет для предыдущих предприятий
        remaining_j = remaining_j - k

    return max_profit, distribution


def get_investment_stats(investments, profits, distribution):
    """
    Подсчитывает детальную статистику по инвестициям и прибыли.

    Args:
        investments (list): Список возможных сумм инвестиций
        profits (list): Матрица прибылей для каждого предприятия
        distribution (list): Список распределения инвестиций по предприятиям

    Returns:
        dict: Словарь с детальной статистикой
    """
    stats = {}
    stats['total_investment'] = sum(distribution)

    enterprise_details = []
    total_profit = 0

    for i, invest in enumerate(distribution):
        profit = get_profit(profits, investments, i, invest) if invest in investments else 0
        total_profit += profit
        enterprise_details.append({
            'enterprise_id': i + 1,
            'investment': invest,
            'profit': profit,
            'roi': (profit / invest if invest > 0 else 0)
        })

    stats['total_profit'] = total_profit
    stats['roi'] = total_profit / stats['total_investment'] if stats['total_investment'] > 0 else 0
    stats['enterprises'] = enterprise_details

    return stats


def run_investment_optimization(data_source, is_file=True):
    """
    Запускает полный процесс оптимизации инвестиций.

    Args:
        data_source: Путь к файлу или двумерный массив данных
        is_file (bool): Если True, data_source это путь к файлу, иначе - двумерный массив

    Returns:
        dict: Результаты оптимизации с детальной статистикой
    """
    # Загрузка данных
    if is_file:
        investments, profits = load_data_from_excel(data_source)
    else:
        investments, profits = load_data_from_array(data_source)

    # Оптимизация
    max_profit, distribution = optimize_investments(investments, profits)

    # Формирование результата
    result = {
        'max_profit': max_profit,
        'distribution': distribution,
        'statistics': get_investment_stats(investments, profits, distribution)
    }

    return result


# Пример использования
if __name__ == "__main__":
    # Запуск оптимизации напрямую с массивом данных
    result = run_investment_optimization(
        data_source='example.xlsx',
        is_file=True
    )

    # Вывод результатов
    print(f"Максимальная суммарная прибыль: {result['max_profit']}")
    print("\nОптимальное распределение инвестиций:")
    for idx, val in enumerate(result['distribution'], start=1):
        print(f"Предприятие {idx}: {val} млн")
