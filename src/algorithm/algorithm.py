from io import BytesIO

import pandas as pd

from src.backend.db.schemas.investments_results import (
    InvestmentStatisticsSchema
)


class InvestmentOptimizer:

    @classmethod
    def load_data_from_excel(cls, file_path):
        """
        Загружает данные из Excel файла по пути.

        Args:
            file_path (str): Путь к Excel файлу с данными

        Returns:
            tuple: (investments, profits)
        """
        df = pd.read_excel(file_path, header=None)
        profit_table = df.values.tolist()

        investments = [row[0] for row in profit_table]
        profits = [row[1:] for row in profit_table]
        return investments, profits

    @classmethod
    def load_data_from_excel_bytes(cls, file_bytes):
        """
        Загружает данные из Excel файла, переданного в виде байтов.

        Args:
            file_bytes (bytes): Байты Excel файла

        Returns:
            tuple: (investments, profits)
        """
        try:
            excel_io = BytesIO(file_bytes)
            df = pd.read_excel(excel_io, header=None)
        except Exception as e:
            raise ValueError(f"Ошибка при чтении Excel: {e}")

        profit_table = df.values.tolist()
        investments = [row[0] for row in profit_table]
        profits = [row[1:] for row in profit_table]
        return investments, profits

    @classmethod
    def load_data_from_array(cls, data_array):
        """
        Загружает данные из двумерного массива.
        """
        investments = [row[0] for row in data_array]
        profits = [row[1:] for row in data_array]
        return investments, profits

    @classmethod
    def get_profit(cls, profits, investments, e, x):
        """
        Получает прибыль, если вложить x млн в e-е предприятие.
        """
        i = investments.index(x)
        return profits[i][e]

    @classmethod
    def optimize_investments(cls, investments, profits):
        """
        Оптимизирует распределение инвестиций между предприятиями с использованием динамического программирования.
        """
        num_enterprises = len(profits[0])
        num_invest_levels = len(investments)

        dp = [[0] * num_invest_levels for _ in range(num_enterprises + 1)]
        choice = [[0] * num_invest_levels for _ in range(num_enterprises + 1)]

        for i in range(1, num_enterprises + 1):
            for j in range(num_invest_levels):
                best_profit = 0
                best_k = 0
                for k in range(j + 1):
                    invest_in_this = investments[k]
                    current_profit = dp[i-1][j-k] + cls.get_profit(profits, investments, i-1, invest_in_this)
                    if current_profit > best_profit:
                        best_profit = current_profit
                        best_k = k
                dp[i][j] = best_profit
                choice[i][j] = best_k

        max_profit = dp[num_enterprises][num_invest_levels - 1]
        distribution = [0] * num_enterprises
        remaining_j = num_invest_levels - 1
        for i in range(num_enterprises, 0, -1):
            k = choice[i][remaining_j]
            distribution[i - 1] = investments[k]
            remaining_j -= k

        return max_profit, distribution

    @classmethod
    def get_investment_stats(
        cls,
        investments,
        profits,
        distribution
    ) -> InvestmentStatisticsSchema:
        """
        Подсчитывает детальную статистику по инвестициям и прибыли.
        """
        stats = {}
        stats['total_investment'] = sum(distribution)

        enterprise_details = []
        total_profit = 0

        for i, invest in enumerate(distribution):
            profit = cls.get_profit(profits, investments, i, invest) if invest in investments else 0
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

    @classmethod
    def run_investment_optimization(cls, data_source, is_file=True):
        """
        Запускает полный процесс оптимизации инвестиций.
        """
        if is_file:
            # data_source - путь к файлу
            investments, profits = cls.load_data_from_excel(data_source)
        else:
            # data_source - двумерный массив
            investments, profits = cls.load_data_from_array(data_source)

        max_profit, distribution = cls.optimize_investments(investments, profits)
        result = {
            'max_profit': max_profit,
            'distribution': distribution,
            'statistics': cls.get_investment_stats(investments, profits, distribution)
        }
        return result


# Пример использования
if __name__ == "__main__":
    # Запуск оптимизации напрямую с массивом данных
    result = InvestmentOptimizer.run_investment_optimization(
        data_source='example.xlsx',
        is_file=True
    )

    # Вывод результатов
    print(f"Максимальная суммарная прибыль: {result['max_profit']}")
    print("\nОптимальное распределение инвестиций:")
    for idx, val in enumerate(result['distribution'], start=1):
        print(f"Предприятие {idx}: {val} млн")
