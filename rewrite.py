import re
import sys

def rewrite():
    path = 'main/java/com/spendwise/SpendWiseServer.java'
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace expense terminology
    code = code.replace('expenses', 'meals')
    code = code.replace('expense_', 'meal_')
    code = code.replace('expense', 'meal')
    code = code.replace('Expenses', 'Meals')
    code = code.replace('Expense', 'Meal')
    code = code.replace('amount', 'calories')

    # Update Categories
    code = re.sub(r'Set\.of\([^)]+\)', 'Set.of("Breakfast", "Lunch", "Dinner", "Snack")', code, count=1)

    # Replace budget terminology
    code = code.replace('budgets', 'calorie_goals')
    code = code.replace('budget_year', 'goal_year')
    code = code.replace('budget_month', 'goal_month')
    code = code.replace('budget', 'goal')
    code = code.replace('Budget', 'Goal')
    code = code.replace('12000', '2000') # default daily calories
    code = code.replace('500000', '10000') # max calories

    # Replace investment terminology with water tracking
    code = code.replace('investments', 'water_logs')
    code = code.replace('investment', 'waterLog')
    code = code.replace('Investment', 'WaterLog')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    rewrite()
    print("Done")
