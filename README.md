# Homework on "Graphs and Trees"

Greetings 🌞
This homework consists of two independent tasks. You will practice applying the maximum flow algorithm to model logistics networks, analyzing optimal product flow routes, and identifying network constraints. Additionally, you will compare the performance of OOBTree and dict data structures for range queries, assessing their efficiency in storing and accessing large datasets.

Ready? Let's get started!

Good luck! 😎

***

## Task 1: Applying the Maximum Flow Algorithm for Logistics Optimization

Develop a program to model a product flow network from warehouses to stores using the maximum flow algorithm. Analyze the obtained results and compare them with theoretical knowledge.

### Task Description

Construct a graph model representing the flow network with the following structure:

![asd](./assets/task.png)

The connections and bandwidths in the graph have the following form:

|From|To|Capacity (units)|
| -- | -- | -- |
| Terminal 1 | Warehouse 1 | 25 |
| Terminal 1 | Warehouse 2 | 20 |
| Terminal 1 | Warehouse 3 | 15 |
| Terminal 2 | Warehouse 3 | 15 |
| Terminal 2 | Warehouse 4 | 30 |
| Terminal 2 | Warehouse 2 | 10 |
| Warehouse 1 | Store 1 | 15 |
| Warehouse 1 | Store 2 | 10 |
| Warehouse 1 | Store 3 | 20 |
| Warehouse 2 | Store 4 | 15 |
| Warehouse 2 | Store 5 | 10 |
| Warehouse 2 | Store 6 | 25 |
| Warehouse 3 | Store 7 | 20 |
| Warehouse 3 | Store 8 | 15 |
| Warehouse 3 | Store 9 | 10 |
| Warehouse 4 | Store 10 | 20 |
| Warehouse 4 | Store 11 | 10 |
| Warehouse 4 | Store 12 | 15 |
| Warehouse 4 | Store 13 | 5 |
| Warehouse 4 | Store 14 | 10 |

Apply the Edmonds-Karp algorithm to determine the maximum flow in the graph. Develop a program that implements this algorithm or use an existing implementation.

### Technical Requirements

1. Use the Edmonds-Karp algorithm to compute the maximum flow.
2. The graph must have 20 vertices and the defined capacities.

### Acceptance Criteria

📌 **Your homework must meet the acceptance criteria to be reviewed by a mentor. If any criteria are missing, the assignment will be returned for revision.**

1. The program correctly calculates the maximum flow and returns accurate results.
2. The data is correctly structured to match the given logistics network.
3. The explanation and analysis are clear and well-structured.
4. The report includes an analysis of the obtained results.

Your report must include a table of final flow values between terminals and stores:

|Terminal|Store|Actual Flow (units)|
| Terminal 1 | Store 1 | X |
| Terminal 1 | Store 2 | Y |
| ... | ... | ... |
| Terminal 2 | Store 14 | Z |

Then, answer the following questions:

1. Which terminals deliver the largest product flow to stores?
2. Which routes have the lowest capacity, and how does this impact the total flow?
3. Which stores received the least supply, and can this be improved by increasing certain route capacities?
4. Are there bottlenecks that could be eliminated to improve logistics efficiency?

***

## Task 2: Performance Comparison of OOBTree and Dict for Range Queries

Develop a program to store a large dataset of products in two data structures—OOBTree and dict—and conduct a comparative performance analysis of their range query execution.

### Task Description

1. Load product data from `generated_items_data.csv`. Each product has:

- ID (unique identifier)
- Name (product name)
- Category
- Price

2. Implement two storage structures:

- **OOBTree** (from the `BTrees` library), where the key is `ID`, and the value is a dictionary of product attributes.
- **dict** (standard dictionary) with the same structure.

3. Create functions to add products to both structures:

- `add_item_to_tree`
- `add_item_to_dict`

4. Implement functions for range queries (find products within a given price range):

- `range_query_tree`
- `range_query_dict`

5. Measure execution time using timeit:

- Perform 100 range queries for each structure.
- Compute the average execution time.

6. Print the total execution time for 100 queries in each structure.

### Technical Requirements

1. Use only `OOBTree` and dict.
2. Implement separate functions for:
  - Adding data (`add_item_to_tree`, `add_item_to_dict`)
  - Range queries (`range_query_tree`, `range_query_dict`)
3. Use timeit for accurate performance measurement.
4. 100 range queries must be executed for each structure.

### Acceptance Criteria

1. The program correctly executes range queries for both structures.
2. Data is correctly added to each structure.
3. OOBTree uses `.items(min, max)` for efficient range queries.
4. dict performs linear search for range queries.
5. Execution time results for both structures are correctly displayed.

Expected Output Format:
```python
Total range_query time for OOBTree: X.XXXXXX seconds
Total range_query time for Dict: X.XXXXXX seconds
```
OOBTree is expected to show better performance due to its sorted structure.
