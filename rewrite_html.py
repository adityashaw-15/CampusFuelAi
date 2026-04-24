import re

def rewrite():
    path = '../index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Title and branding
    html = html.replace('SpendWise AI | Student Expense Tracker', 'NutriWise AI | Student Nutrition Tracker')
    html = html.replace('SpendWise AI', 'NutriWise AI')
    html = html.replace('AI-powered money clarity for students.', 'AI-powered nutrition clarity for students.')
    html = html.replace('Track daily spending, predict month-end balance, spot unusual expenses', 'Track daily meals, predict macro balance, spot unhealthy habits')
    html = html.replace('save everything in a Java SQL backend', 'save everything in a Java SQL backend')
    html = html.replace('AI expense tracker preview', 'AI nutrition tracker preview')
    
    # Receipts -> Meals in Hero Visual
    html = html.replace('<span>Mess</span>\n              <strong>-₹120</strong>', '<span>Oatmeal</span>\n              <strong>350 kcal</strong>')
    html = html.replace('<span>Books</span>\n              <strong>-₹450</strong>', '<span>Salad</span>\n              <strong>250 kcal</strong>')
    html = html.replace('<span>Saved</span>\n              <strong>₹1.8k</strong>', '<span>Remaining</span>\n              <strong>1200 kcal</strong>')

    # Dashboard labels
    html = html.replace('Expense tracker dashboard', 'Nutrition tracker dashboard')
    html = html.replace('Today&apos;s student budget cockpit', 'Today&apos;s calorie cockpit')
    
    html = html.replace('Monthly budget', 'Daily Calorie Goal')
    html = html.replace('₹12,000', '2000 kcal')
    html = html.replace('Parent allowance + part-time income', 'Based on fitness profile')

    html = html.replace('Spent so far', 'Calories Consumed')
    html = html.replace('₹0', '0 kcal')
    html = html.replace('Across all categories', 'Across all meals')

    html = html.replace('AI forecast', 'Remaining Calories')
    html = html.replace('Projected month-end balance', 'For the rest of the day')

    html = html.replace('Risk score', 'Health Score')
    html = html.replace('Low', '10/10')
    html = html.replace('Based on pace and anomalies', 'Based on goal adherence')

    # Add form
    html = html.replace('Add expense', 'Log meal')
    html = html.replace('expenseName', 'mealName')
    html = html.replace('expenseAmount', 'mealCalories')
    html = html.replace('expenseCategory', 'mealCategory')
    html = html.replace('expenseDate', 'mealDate')
    html = html.replace('expenseForm', 'mealForm')
    html = html.replace('expenseSubmitText', 'mealSubmitText')
    
    html = html.replace('<span>Item</span>', '<span>Food Item</span>')
    html = html.replace('Campus coffee', 'Campus salad')
    html = html.replace('<span>Amount</span>', '<span>Calories (kcal)</span>')
    html = html.replace('placeholder="80"', 'placeholder="350"')
    
    html = re.sub(r'<select id="mealCategory" name="mealCategory" required>.*?</select>', 
                  '<select id="mealCategory" name="mealCategory" required><option value="Breakfast">Breakfast</option><option value="Lunch">Lunch</option><option value="Dinner">Dinner</option><option value="Snack">Snack</option></select>', 
                  html, flags=re.DOTALL)
    
    html = html.replace('Budget setting', 'Goal setting')
    html = html.replace('Budget limit', 'Daily goal')
    html = html.replace('min="5000" max="30000" step="500" value="12000"', 'min="1200" max="4000" step="50" value="2000"')

    # Charts
    html = html.replace('Expense charts', 'Nutrition charts')
    html = html.replace('data-chart-mode="amount">₹', 'data-chart-mode="amount">kcal')
    html = html.replace('Monthly expense chart', 'Monthly calorie chart')

    # AI Coach
    html = html.replace('AI money coach', 'AI Nutrition Coach')
    html = html.replace('Ask me anything about your spending habits!', 'Ask me anything about your diet and nutrition!')
    html = html.replace('Can I afford pizza tonight?', 'Should I eat pizza tonight?')

    # Recent list
    html = html.replace('Recent expenses', 'Recent meals')
    html = html.replace('expenseList', 'mealList')
    html = html.replace('expense-list', 'meal-list')

    # Missions
    html = html.replace('Savings missions', 'Health missions')

    # Markets
    html = html.replace('Market watch & investments', 'Water & Weight log')
    html = html.replace('Live provider when API key is configured, safe demo quotes otherwise.', 'Log your daily hydration and weight progress.')
    html = html.replace('₹ Budget', '🎯 Goals')
    html = html.replace('₹ Savings', '🔥 Calories')
    html = html.replace('₹ SQL Ledger', '🗄️ SQL Ledger')
    html = html.replace('₹ Market Watch', '💧 Water')
    
    html = html.replace('marketList', 'healthTips')
    html = html.replace('Stock symbol', 'Metric')
    html = html.replace('Exchange', 'Time')
    html = html.replace('Amount to track', 'Value')
    html = html.replace('investAmount', 'waterAmount')
    html = html.replace('investNote', 'waterNote')
    html = html.replace('Track investment', 'Track health metric')
    html = html.replace('Educational tracker only. It does not place real trades or provide guaranteed investment advice.', 'Log water in glasses (e.g., 8).')

    # Login
    html = html.replace('Open your personal money ledger.', 'Open your personal nutrition ledger.')
    html = html.replace('SQL expenses, budgets, and investments', 'SQL meals, goals, and health logs')
    
    # Pitch
    html = html.replace('helps students spend with confidence.', 'helps students eat with confidence.')
    html = html.replace('Students lose track of small daily spends until the budget suddenly disappears.', 'Students lose track of small snacks until their daily calories run out.')
    html = html.replace('AI forecasts, detects unusual expenses, and suggests realistic saving actions.', 'AI tracks calories, detects unhealthy habits, and suggests realistic diet changes.')
    html = html.replace('fewer end-month shocks, and clearer financial habits.', 'better energy levels, and clearer dietary habits.')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    rewrite()
    print("Done")
