# Bank Management System in Python

class Customer:
    def __init__(self, customer_id, name, address, phone):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Address: {self.address}, Phone: {self.phone}"


class Account:
    def __init__(self, account_id, customer_id, balance=0):
        self.account_id = account_id
        self.customer_id = customer_id
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return self.balance
        else:
            return "Insufficient funds"

    def __str__(self):
        return f"Account ID: {self.account_id}, Customer ID: {self.customer_id}, Balance: {self.balance}"


class Transaction:
    def __init__(self, transaction_id, account_id, amount, transaction_type):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Account ID: {self.account_id}, Amount: {self.amount}, Type: {self.transaction_type}"


class BankManagementSystem:
    def __init__(self):
        self.customers = {}
        self.accounts = {}
        self.transactions = []
        self.customer_counter = 1
        self.account_counter = 1
        self.transaction_counter = 1

    def add_customer(self, name, address, phone):
        customer_id = self.customer_counter
        self.customer_counter += 1
        self.customers[customer_id] = Customer(customer_id, name, address, phone)
        return customer_id

    def update_customer(self, customer_id, name=None, address=None, phone=None):
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            if name:
                customer.name = name
            if address:
                customer.address = address
            if phone:
                customer.phone = phone
            return True
        return False

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            del self.customers[customer_id]
            return True
        return False

    def view_customer(self, customer_id):
        return self.customers.get(customer_id, "Customer not found")

    def create_account(self, customer_id, initial_balance=0):
        if customer_id in self.customers:
            account_id = self.account_counter
            self.account_counter += 1
            self.accounts[account_id] = Account(account_id, customer_id, initial_balance)
            return account_id
        return "Customer not found"

    def update_account(self, account_id, balance=None):
        if account_id in self.accounts:
            account = self.accounts[account_id]
            if balance is not None:
                account.balance = balance
            return True
        return False

    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False

    def view_account(self, account_id):
        return self.accounts.get(account_id, "Account not found")

    def deposit(self, account_id, amount):
        if account_id in self.accounts:
            new_balance = self.accounts[account_id].deposit(amount)
            self.transactions.append(Transaction(self.transaction_counter, account_id, amount, "Deposit"))
            self.transaction_counter += 1
            return new_balance
        return "Account not found"

    def withdraw(self, account_id, amount):
        if account_id in self.accounts:
            result = self.accounts[account_id].withdraw(amount)
            if result != "Insufficient funds":
                self.transactions.append(Transaction(self.transaction_counter, account_id, amount, "Withdrawal"))
                self.transaction_counter += 1
            return result
        return "Account not found"

    def transfer(self, from_account_id, to_account_id, amount):
        if from_account_id in self.accounts and to_account_id in self.accounts:
            result = self.accounts[from_account_id].withdraw(amount)
            if result != "Insufficient funds":
                self.accounts[to_account_id].deposit(amount)
                self.transactions.append(Transaction(self.transaction_counter, from_account_id, amount, "Transfer Out"))
                self.transactions.append(Transaction(self.transaction_counter, to_account_id, amount, "Transfer In"))
                self.transaction_counter += 1
                return "Transfer successful"
            return result
        return "Account not found"

    def generate_customer_report(self, customer_id):
        customer = self.view_customer(customer_id)
        if customer == "Customer not found":
            return customer
        report = str(customer) + "\nAccounts:\n"
        for account_id, account in self.accounts.items():
            if account.customer_id == customer_id:
                report += str(account) + "\n"
        return report

    def generate_account_report(self, account_id):
        account = self.view_account(account_id)
        if account == "Account not found":
            return account
        report = str(account) + "\nTransactions:\n"
        for transaction in self.transactions:
            if transaction.account_id == account_id:
                report += str(transaction) + "\n"
        return report

    def generate_transaction_report(self):
        report = "All Transactions:\n"
        for transaction in self.transactions:
            report += str(transaction) + "\n"
        return report


# Main Program
def main():
    bank = BankManagementSystem()

    while True:
        print("\nBank Management System")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Delete Customer")
        print("4. View Customer")
        print("5. Create Account")
        print("6. Update Account")
        print("7. Delete Account")
        print("8. View Account")
        print("9. Deposit")
        print("10. Withdraw")
        print("11. Transfer")
        print("12. Generate Customer Report")
        print("13. Generate Account Report")
        print("14. Generate Transaction Report")
        print("15. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter customer name: ")
            address = input("Enter customer address: ")
            phone = input("Enter customer phone: ")
            customer_id = bank.add_customer(name, address, phone)
            print(f"Customer added successfully with ID: {customer_id}")

        elif choice == "2":
            customer_id = int(input("Enter customer ID: "))
            name = input("Enter new name (leave blank to skip): ")
            address = input("Enter new address (leave blank to skip): ")
            phone = input("Enter new phone (leave blank to skip): ")
            if bank.update_customer(customer_id, name or None, address or None, phone or None):
                print("Customer updated successfully")
            else:
                print("Customer not found")

        elif choice == "3":
            customer_id = int(input("Enter customer ID: "))
            if bank.delete_customer(customer_id):
                print("Customer deleted successfully")
            else:
                print("Customer not found")

        elif choice == "4":
            customer_id = int(input("Enter customer ID: "))
            print(bank.view_customer(customer_id))

        elif choice == "5":
            customer_id = int(input("Enter customer ID: "))
            initial_balance = float(input("Enter initial balance: "))
            account_id = bank.create_account(customer_id, initial_balance)
            if account_id != "Customer not found":
                print(f"Account created successfully with ID: {account_id}")
            else:
                print("Customer not found")

        elif choice == "6":
            account_id = int(input("Enter account ID: "))
            balance = float(input("Enter new balance: "))
            if bank.update_account(account_id, balance):
                print("Account updated successfully")
            else:
                print("Account not found")

        elif choice == "7":
            account_id = int(input("Enter account ID: "))
            if bank.delete_account(account_id):
                print("Account deleted successfully")
            else:
                print("Account not found")

        elif choice == "8":
            account_id = int(input("Enter account ID: "))
            print(bank.view_account(account_id))

        elif choice == "9":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            result = bank.deposit(account_id, amount)
            print(f"New balance: {result}")

        elif choice == "10":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            result = bank.withdraw(account_id, amount)
            print(f"New balance: {result}")

        elif choice == "11":
            from_account_id = int(input("Enter source account ID: "))
            to_account_id = int(input("Enter destination account ID: "))
            amount = float(input("Enter amount to transfer: "))
            result = bank.transfer(from_account_id, to_account_id, amount)
            print(result)

        elif choice == "12":
            customer_id = int(input("Enter customer ID: "))
            print(bank.generate_customer_report(customer_id))

        elif choice == "13":
            account_id = int(input("Enter account ID: "))
            print(bank.generate_account_report(account_id))

        elif choice == "14":
            print(bank.generate_transaction_report())

        elif choice == "15":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()