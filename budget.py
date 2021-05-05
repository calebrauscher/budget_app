class Category:

  def __init__(self, name, ledger=None):
    if ledger == None:
      self.ledger = []
    self.name = name
    self.total = 0

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.total += amount

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": 0-amount, "description": description})
      self.total -= amount
      return True
    return False

  def get_balance(self):
    return self.total

  def transfer(self, amount, other):
    if self.check_funds(amount):
      self.withdraw(amount, description=f"Transfer to {other.name}")
      other.deposit(amount, description=f"Transfer from {self.name}")
      return True
    return False

  def check_funds(self, amount):
    return amount <= self.get_balance()

  def __str__(self):
    output = ""
    stars = int((30 - len(self.name))/2)
    output = "*" * stars + self.name + "*" * stars + "\n"
    for item in self.ledger:
      description = item["description"][:23]
      money = str(item["amount"]) if isinstance(item["amount"], float) else (str(item["amount"]) + ".00")
      spaces = 30 - len(description) - len(money)

      output = output + description + " " * spaces + money + "\n"
    output = output + f"Total: {self.get_balance()}"
    return output


def create_spend_chart(categories):
  percent_category = {}
  total_spent = 0
  yaxis = ["100", " 90", " 80", " 70", " 60", " 50", " 40", " 30", " 20", " 10", "  0"]

  for category in categories:
    total_spent += abs(sum([trans["amount"] for trans in category.ledger if trans["amount"] < 0]))
    percent_category[category.name] = abs(sum([trans["amount"] for trans in category.ledger if trans["amount"] < 0]))

  for k,v in percent_category.items():
    percent_category[k] = int(percent_category[k]/total_spent * 10) * 10

  chart = "Percentage spent by category\n"
  for tick in yaxis:
    chart = chart + tick + "| "
    for k,v in percent_category.items():
      if percent_category[k] >= int(tick.strip()):
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"
  chart += "    ----------\n"

  names = [category.name for category in categories]
  max_letters = max([len(name) for name in names])
  for i in range(max_letters):
    chart += "     "
    for name in names:
      try:
        chart = chart + name[i] + "  "
      except IndexError:
        chart += "   "
    chart += "\n"
  
  return chart[:-1]