import csv
import timeit
from BTrees.OOBTree import OOBTree
import matplotlib.pyplot as plt
import numpy as np

# Функція для завантаження даних з CSV файлу
def load_items_data(filename):
    items = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append(item)
    return items

# Функція для додавання елемента в OOBTree
def add_item_to_tree(tree, item):
    tree.insert(item["ID"], item)

# Функція для додавання елемента в dict
def add_item_to_dict(items_dict, item):
    items_dict[item["ID"]] = item

# Функція для діапазонного запиту для OOBTree
def range_query_tree(tree, min_price, max_price):
    result = []
    for key, value in tree.items(min_price, max_price):
        if min_price <= value["Price"] <= max_price:
            result.append(value)
    return result

# Функція для діапазонного запиту для dict
def range_query_dict(items_dict, min_price, max_price):
    result = []
    for item in items_dict.values():
        if min_price <= item["Price"] <= max_price:
            result.append(item)
    return result

# Функція для візуалізації результатів
def visualize_results(oobtree_time, dict_time):
    plt.figure(figsize=(10, 6))
    
    # Створення стовпчикової діаграми
    structures = ['OOBTree', 'Dictionary']
    times = [oobtree_time, dict_time]
    
    bars = plt.bar(structures, times)
    
    # Додавання кольорів
    bars[0].set_color('#2ecc71')  # зелений для OOBTree
    bars[1].set_color('#e74c3c')  # червоний для Dictionary
    
    # Додавання значень над стовпцями
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}s',
                ha='center', va='bottom')
    
    # Налаштування графіка
    plt.title('Performance Comparison: OOBTree vs Dictionary')
    plt.ylabel('Time (seconds)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Додавання відсоткової різниці
    percent_diff = abs(oobtree_time - dict_time) / max(oobtree_time, dict_time) * 100
    faster_struct = "OOBTree" if oobtree_time < dict_time else "Dictionary"
    plt.figtext(0.5, -0.1, 
                f'{faster_struct} is faster by {percent_diff:.2f}%',
                ha='center', va='center')
    
    plt.tight_layout()
    return plt.gcf()

# Основна функція для порівняння
def compare_structures(filename):
    # Завантаження даних
    items = load_items_data(filename)
    
    # Створення OOBTree і dict
    tree = OOBTree()
    items_dict = {}
    
    # Додавання елементів у OOBTree та dict
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(items_dict, item)
    
    # Функція для вимірювання часу діапазонного запиту для OOBTree
    def time_range_query_tree():
        return range_query_tree(tree, 10, 100)
    
    # Функція для вимірювання часу діапазонного запиту для dict
    def time_range_query_dict():
        return range_query_dict(items_dict, 10, 100)
    
    # Вимірювання часу для 100 діапазонних запитів
    oobtree_time = timeit.timeit(time_range_query_tree, number=100)
    dict_time = timeit.timeit(time_range_query_dict, number=100)
    
    # Виведення результатів
    print(f"Total range_query time for OOBTree: {oobtree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
    
    if oobtree_time < dict_time:
        print("OOBTree is faster than Dict for range queries!")
    else:
        print("Dict is faster than OOBTree for range queries!")
    
    # Візуалізація результатів
    figure = visualize_results(oobtree_time, dict_time)
    plt.show()
    
    return oobtree_time, dict_time

if __name__ == "__main__":
    # Шлях до файлу з даними
    filename = "generated_items_data.csv"
    # Порівняння структур
    compare_structures(filename)