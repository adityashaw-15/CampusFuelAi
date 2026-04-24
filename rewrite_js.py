import re

def rewrite():
    path = '../app.js'
    with open(path, 'r', encoding='utf-8') as f:
        js = f.read()

    # Constants & Storage Keys
    js = js.replace('spendwise', 'nutriwise')
    js = js.replace('INR.format', 'String')
    
    # Currency formatter (remove it and replace with something simpler)
    # We can just change INR formatter to append 'kcal'
    js = js.replace('const INR = new Intl.NumberFormat("en-IN", {', 'const INR = { format: (val) => val + " kcal" };\n/*')
    js = js.replace('maximumFractionDigits: 0\n});', '*/')

    # Categories and Colors
    js = js.replace('Food: "#d9a928",\n  Transport: "#f1d36b",\n  Trip: "#f6cf63",\n  Study: "#b8860b",\n  Hostel: "#7f6a2f",\n  Fun: "#f6b64b",\n  Health: "#c9f27c"', 'Breakfast: "#8bc34a",\n  Lunch: "#4caf50",\n  Dinner: "#388e3c",\n  Snack: "#cddc39"')
    
    # Demo Data Replacement
    # replace demoExpenseRows with simple meals
    demo_meals = """const demoExpenseRows = [
  { name: "Oatmeal", amount: 350, category: "Breakfast", date: `${currentYear}-01-05` },
  { name: "Chicken Salad", amount: 450, category: "Lunch", date: `${currentYear}-01-08` },
  { name: "Pasta", amount: 600, category: "Dinner", date: `${currentYear}-01-18` },
  { name: "Apple", amount: 95, category: "Snack", date: `${currentYear}-01-24` },
  { name: "Eggs", amount: 200, category: "Breakfast", date: `${currentYear}-02-07` },
  { name: "Sandwich", amount: 500, category: "Lunch", date: `${currentYear}-02-12` }
];"""
    js = re.sub(r'const demoExpenseRows = \[.*?\];', demo_meals, js, flags=re.DOTALL)

    # General replacements
    js = js.replace('expenses', 'meals')
    js = js.replace('expense', 'meal')
    js = js.replace('Expenses', 'Meals')
    js = js.replace('Expense', 'Meal')
    
    js = js.replace('investments', 'waterLogs')
    js = js.replace('investment', 'waterLog')
    js = js.replace('Investments', 'WaterLogs')
    js = js.replace('Investment', 'WaterLog')

    js = js.replace('budget', 'goal')
    js = js.replace('Budget', 'Goal')

    js = js.replace('marketQuotes', 'healthTips')
    js = js.replace('marketSource', 'tipSource')
    js = js.replace('marketList', 'healthTipsList')
    
    # Values
    js = js.replace('12000', '2000') # default goal

    # API endpoints
    js = js.replace('/api/markets?symbols=AAPL,MSFT,IBM,TSLA,RELIANCE.BSE', '/api/health_tips')

    # AI Prompt change
    js = js.replace('Ask me anything about your spending habits!', 'Ask me anything about your diet and nutrition!')
    js = js.replace('Can I afford pizza tonight?', 'Should I eat pizza tonight?')

    # Calculate 10-point daily score
    # We will inject some custom logic in renderInsights to show the 10 point score
    js = js.replace('riskValue.textContent = risk.label;', 'riskValue.textContent = calculateHealthScore(totals.spent, goal) + "/10";')
    
    score_logic = """
function calculateHealthScore(consumed, target) {
  if (target === 0) return 10;
  const ratio = consumed / target;
  if (ratio > 1.2 || ratio < 0.5) return 4;
  if (ratio > 1.1 || ratio < 0.75) return 7;
  return 10;
}
"""
    if "calculateHealthScore" not in js:
        js += score_logic

    with open(path, 'w', encoding='utf-8') as f:
        f.write(js)

if __name__ == '__main__':
    rewrite()
    print("Done")
