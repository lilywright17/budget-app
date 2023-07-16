class Category:
  
  def __init__(self, name):
      self.name = name
      self.ledger = []
      self.balance = 0

  def __repr__(self):
    header = f"{self.name:*^30}\n"
    table = ""
    total = 0
    for item in self.ledger:
      table += f"{item['description']:<23.23}" + f"{item['amount']:>7.2f}" + "\n"
      total += item['amount']
    output = header + table + 'Total: ' + str(total)
    return output
    
  #deposit method that accepts an amount and description. if no description is given, default to an empty string. should append an object to the ledger list in the form of {"amount": amount, "description": description}.
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount

  #withdraw method similar to the deposit method, the amount passed in should be stored in the ledger as a negative number. not enough funds, nothing added to the ledger. should return True if the withdrawal took place, and False otherwise.
  def withdraw(self, amount, description=""):
    if (self.check_funds(amount)):
      self.ledger.append({"amount": -amount, "description": description})
      self.balance -= amount
      return True
    else: 
      return False
      
  #transfer method that accepts an amount and another budget category as arguments. should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". if there are not enough funds, nothing should be added to either ledgers. method should return True if the transfer took place, and False otherwise.
  def transfer(self, amount, category):
    if (self.check_funds(amount)):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False
      
#get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred
  def get_balance(self):
    return self.balance

  #check_funds method that accepts an amount as an argument. returns False if the amount is greater than the balance of the budget category and returns True otherwise. method should be used by both the withdraw method and transfer method.
  def check_funds(self, amount):
    if self.balance - amount >= 0:
      return True
    else:
      return False

def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
