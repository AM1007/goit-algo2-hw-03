import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate
from colorama import init, Fore
from collections import defaultdict, deque

# Ініціалізація colorama
init()

class LogisticsNetwork:
    def __init__(self):
        self.G = nx.DiGraph()
        self.setup_network()

    def setup_network(self):
        # Додавання вузлів з атрибутами для позиціонування
        terminals = ['Terminal 1', 'Terminal 2']
        warehouses = ['Warehouse 1', 'Warehouse 2', 'Warehouse 3', 'Warehouse 4']
        stores = [f'Store {i}' for i in range(1, 15)]

        # Додавання вузлів з атрибутами шару для правильного позиціонування
        for i, terminal in enumerate(terminals):
            self.G.add_node(terminal, layer=0, pos=(0, i))
            
        for i, warehouse in enumerate(warehouses):
            self.G.add_node(warehouse, layer=1, pos=(1, i))
            
        for i, store in enumerate(stores):
            self.G.add_node(store, layer=2, pos=(2, i))

        # Додавання ребер з пропускною здатністю
        edges_capacity = [
            # Від терміналів до складів
            ('Terminal 1', 'Warehouse 1', 25),
            ('Terminal 1', 'Warehouse 2', 20),
            ('Terminal 1', 'Warehouse 3', 15),
            ('Terminal 2', 'Warehouse 3', 15),
            ('Terminal 2', 'Warehouse 4', 30),
            ('Terminal 2', 'Warehouse 2', 10),
            
            # Від складів до магазинів
            ('Warehouse 1', 'Store 1', 15),
            ('Warehouse 1', 'Store 2', 10),
            ('Warehouse 1', 'Store 3', 20),
            ('Warehouse 2', 'Store 4', 15),
            ('Warehouse 2', 'Store 5', 10),
            ('Warehouse 2', 'Store 6', 25),
            ('Warehouse 3', 'Store 7', 20),
            ('Warehouse 3', 'Store 8', 15),
            ('Warehouse 3', 'Store 9', 10),
            ('Warehouse 4', 'Store 10', 20),
            ('Warehouse 4', 'Store 11', 10),
            ('Warehouse 4', 'Store 12', 15),
            ('Warehouse 4', 'Store 13', 5),
            ('Warehouse 4', 'Store 14', 10)
        ]

        # Додавання ребер до графа
        for (u, v, capacity) in edges_capacity:
            self.G.add_edge(u, v, capacity=capacity, flow=0)

    def find_path(self, source, sink, path):
        if source == sink:
            return path
        
        for neighbor in self.G.neighbors(source):
            edge_data = self.G[source][neighbor]
            residual_capacity = edge_data['capacity'] - edge_data['flow']
            
            if residual_capacity > 0 and neighbor not in path:
                result = self.find_path(neighbor, sink, path + [neighbor])
                if result is not None:
                    return result
        return None

    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [source])
        while path is not None:
            # Знаходження мінімальної залишкової пропускної здатності на шляху
            flow = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge_data = self.G[u][v]
                flow = min(flow, edge_data['capacity'] - edge_data['flow'])

            # Оновлення потоків
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.G[u][v]['flow'] += flow

            path = self.find_path(source, sink, [source])

    def calculate_all_flows(self):
        total_flow = 0
        flows = []
        
        # Розрахунок потоків для кожного терміналу
        for terminal in ['Terminal 1', 'Terminal 2']:
            for store in [f'Store {i}' for i in range(1, 15)]:
                # Скидання всіх потоків перед новим розрахунком
                for u, v, d in self.G.edges(data=True):
                    d['flow'] = 0
                
                # Розрахунок максимального потоку
                self.max_flow(terminal, store)
                
                # Збір результатів
                store_flow = sum(self.G[u][v]['flow'] for u, v in self.G.in_edges(store))
                if store_flow > 0:
                    flows.append([terminal, store, store_flow])
                    total_flow += store_flow

        return flows, total_flow

    def visualize_network(self):
        plt.figure(figsize=(15, 10))
        
        # Отримання позицій вузлів з атрибутів
        pos = nx.get_node_attributes(self.G, 'pos')
        
        # Малювання вузлів з різними кольорами залежно від шару
        node_colors = []
        for node in self.G.nodes():
            layer = self.G.nodes[node]['layer']
            if layer == 0:
                node_colors.append('lightblue')
            elif layer == 1:
                node_colors.append('lightgreen')
            else:
                node_colors.append('lightpink')
        
        # Малювання вузлів
        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, node_size=700)
        
        # Малювання ребер
        edge_colors = ['red' if d['flow'] > 0 else 'gray' for (u, v, d) in self.G.edges(data=True)]
        nx.draw_networkx_edges(self.G, pos, edge_color=edge_colors)
        
        # Додавання міток
        nx.draw_networkx_labels(self.G, pos)
        edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for (u, v, d) in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels)
        
        plt.title("Logistics Network Flow")
        plt.axis('off')
        plt.show()

def analyze_results(flows):
    # Аналіз по терміналах
    terminal_flows = defaultdict(int)
    store_flows = defaultdict(int)
    
    for flow in flows:
        terminal, store, amount = flow
        terminal_flows[terminal] += amount
        store_flows[store] += amount
    
    print(f"\n{Fore.CYAN}Terminal Analysis:{Fore.RESET}")
    print(tabulate([[terminal, flow] for terminal, flow in terminal_flows.items()],
                  headers=['Terminal', 'Total Flow'],
                  tablefmt='pretty'))
    
    print(f"\n{Fore.CYAN}Stores with Lowest Flow:{Fore.RESET}")
    lowest_stores = sorted(store_flows.items(), key=lambda x: x[1])[:3]
    print(tabulate(lowest_stores, headers=['Store', 'Total Flow'], tablefmt='pretty'))
    
    return terminal_flows, store_flows

def main():
    # Створення та аналіз мережі
    network = LogisticsNetwork()
    flows, total_flow = network.calculate_all_flows()
    
    # Виведення результатів
    print(f"\n{Fore.GREEN}Maximum Flow Analysis Results:{Fore.RESET}")
    print(tabulate(flows, headers=['Terminal', 'Store', 'Flow'], tablefmt='pretty'))
    print(f"\n{Fore.GREEN}Total network flow: {total_flow}{Fore.RESET}")
    
    # Аналіз результатів
    terminal_flows, store_flows = analyze_results(flows)
    
    # Візуалізація мережі
    network.visualize_network()

if __name__ == "__main__":
    main()