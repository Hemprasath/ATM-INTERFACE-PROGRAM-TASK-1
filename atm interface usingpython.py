from datetime import datetime

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance


class Transaction:
    def __init__(self, transaction_type, amount, timestamp):
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp


class TransactionHistory:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction_type, amount):
        timestamp = datetime.now()
        transaction = Transaction(transaction_type, amount, timestamp)
        self.transactions.append(transaction)

    def display_history(self):
        for transaction in self.transactions:
            print(
                f"{transaction.timestamp}: {transaction.transaction_type} - Amount: {transaction.amount}"
            )


class Withdrawal:
    def withdraw(self, user, amount):
        if amount > 0 and amount <= user.balance:
            user.balance -= amount
            return True
        else:
            return False


class Deposit:
    def deposit(self, user, amount):
        if amount > 0:
            user.balance += amount
            return True
        else:
            return False


class Transfer:
    def transfer(self, sender, receiver, amount):
        if amount > 0 and amount <= sender.balance:
            sender.balance -= amount
            receiver.balance += amount
            return True
        else:
            return False


class Quit:
    def quit(self):
        print("Exiting the system. Thank you for using our ATM.")
        exit()


class ATM:
    def __init__(self):
        self.users = {}
        self.transaction_history = TransactionHistory()
        self.withdrawal = Withdrawal()
        self.deposit = Deposit()
        self.transfer = Transfer()
        self.quit_operation = Quit()

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        if user_id in self.users and self.users[user_id].pin == pin:
            return self.users[user_id]
        return None

    def display_menu(self):
        print("\nATM Menu:")
        print("1. Balance Inquiry")
        print("2. Cash Withdrawal")
        print("3. Deposit")
        print("4. Transfer Funds")
        print("5. Transaction History")
        print("6. Quit")

    def execute_operation(self, user, choice):
        if choice == "1":
            print(f"Your balance: {user.balance}")
        elif choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            if self.withdrawal.withdraw(user, amount):
                print("Withdrawal successful.")
                self.transaction_history.add_transaction("Withdrawal", amount)
            else:
                print("Withdrawal failed. Insufficient funds or invalid amount.")
        elif choice == "3":
            amount = float(input("Enter deposit amount: "))
            if self.deposit.deposit(user, amount):
                print("Deposit successful.")
                self.transaction_history.add_transaction("Deposit", amount)
            else:
                print("Deposit failed. Invalid amount.")
        elif choice == "4":
            receiver_id = input("Enter receiver's User ID: ")
            receiver = self.users.get(receiver_id)
            if receiver:
                amount = float(input("Enter transfer amount: "))
                if self.transfer.transfer(user, receiver, amount):
                    print("Transfer successful.")
                    self.transaction_history.add_transaction("Transfer", amount)
                else:
                    print("Transfer failed. Insufficient funds or invalid amount.")
            else:
                print("Receiver not found.")
        elif choice == "5":
            print("\nTransaction History:")
            self.transaction_history.display_history()
        elif choice == "6":
            self.quit_operation.quit()
        else:
            print("Invalid choice. Please choose a valid option.")


# Example usage
if __name__ == "__main__":
    atm = ATM()

    user1 = User("vignesh", "1234", 1000)
    user2 = User("vicky", "8772", 500)

    atm.add_user(user1)
    atm.add_user(user2)

    user_id_input = input("Enter User ID: ")
    pin_input = input("Enter PIN: ")

    current_user = atm.authenticate_user(user_id_input, pin_input)

    if current_user:
        print(f"Authentication successful. Welcome, {current_user.user_id}!")
        while True:
            atm.display_menu()
            user_choice = input("Enter your choice: ")
            atm.execute_operation(current_user, user_choice)
    else:
        print("Authentication failed. Please check your User ID and PIN.")
