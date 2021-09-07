class Category:

  def __init__(self, description):
    self.description = description
    self.ledger = []
    self.balance = 0.0
    
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount
    
  def withdraw(self, amount, description=""):
    if self.balance - amount >= 0:
      self.ledger.append({"amount": -1 * amount, "description": description})
      self.balance -= amount
      return True
    else:
      return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, description_instance):
    if self.withdraw(amount, "Transfer to {}".format(description_instance.description)):
      description_instance.deposit(amount, "Transfer from {}".format(self.description))
      return True
    else:
      return False
  
  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True

  def __str__(self):
    header = self.description.center(30, "*") + "\n"
    ledger = ""
    for i in self.ledger:
      description_name = f"{i['description']:<23}"
      description_amount = f"{i['amount']:>7.2f}"
      ledger += f"{description_name[:23]}{description_amount[:7]}\n"
    footer = "Total: {:.2f}".format(self.balance)
    
    return header + ledger + footer


def create_spend_chart(categories):
  spend_total = []
  for category in categories:
    spend_per_category = 0
    for item in category.ledger:
      if item["amount"] < 0:
        spend_per_category += abs(item["amount"])
    spend_total.append(round(spend_per_category,2))
  
  percent_per_category = []
  for amount in spend_total:
    percent = round(100 * float(amount)/float(round(sum(spend_total),2)))
    percent_per_category.append(percent)
  
  header = "Percentage spent by category\n"
  footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
  
  chart = ""
  for i in range(100, -1, -10):
    chart += f"{str(i)+'|':>4}"
    for percent in percent_per_category:
      if percent >= i:
        chart += " o "
      else:
        chart += "   "
    chart += " \n"

  descriptions = list(map(lambda category: category.description, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
  for x in zip(*descriptions):
    footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"


  return (header + chart + footer).rstrip("\n")


