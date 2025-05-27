'''
Sorry for the excessive comments, jumping back into this after a while so making sure I can remember everything
'''

# Import libraries
import pandas as pd  # For handling CSV data
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus  # PuLP components for optimization




# Read the CSV file containing item names, weights, and values into a pandas dataframe
items = pd.read_csv("items.csv")




# Create linear programming problem
# "name" is a label, and "sense=LpMaximize" used in order to maximize the objective function
model = LpProblem(name="game-inventory-optimization", sense=LpMaximize)




# Create a binary variable for each item: 1 if selected, 0 if not
# creating a dictionary where each item name maps to a PuLP variable
# such as {'Health Potion': LpVariable('Health Potion', cat='Binary'), ...}
item_vars = {
    row.item: LpVariable(name=row.item, cat="Binary")  # 'Binary' so 0 or 1
    for row in items.itertuples()
}




# Want to maximize the total value of selected items
# This sums: (items value X whether its selected [0 or 1]) for all items
# lpSum handles the addition for PuLP
model += (
    lpSum(item_vars[row.item] * row.value for row in items.itertuples()),
    "TotalValue"  # Name for the objective function
)




# Set the maximum allowed weight the player can carry
MAX_WEIGHT = 10

# Add a constraint: total weight of selected items must be less than or equal to MAX_WEIGHT
# sum of (items weight X whether its selected [0 or 1]) for all items
model += (
    lpSum(item_vars[row.item] * row.weight for row in items.itertuples()) <= MAX_WEIGHT,
    "WeightLimit"
)




# tell PuLP to solve the problem
status = model.solve()




# Print the status
print(f"Status: {model.status}, {LpStatus[model.status]}")

# Print the list of items that should be included in the backpack
print("Items to include:")
for item in items.itertuples():
    # Check the value of the variable (0 or 1) to see if the item was selected
    if item_vars[item.item].value() == 1:
        print(f" - {item.item}")
