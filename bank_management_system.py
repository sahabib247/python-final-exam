from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    bank_balance = 0
    loan = True
    loan_count = 0

    def __init__(self, name, email, address, acc_type, password) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.acc_type = acc_type
        self.acc_num = len(Account.accounts) + 1
        self.balance = 0
        self.password = password
        self.transaction = []

        Account.accounts.append(self)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            Account.bank_balance += amount
            self.transaction.append(f'Deposited {amount} Taka')
            print(f'Deposited {amount} Taka. New balance : {self.balance} Taka.')
        else:
            print('Invalid deposit amount!')

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            Account.bank_balance -= amount
            self.transaction.append(f'Withdrew {amount} Taka')
            print(f'Withdrew {amount} Taka. New balance : {self.balance} Taka.')
        elif amount > 0 and self.balance < amount:
            print('Withdrawal amount exceeded!')
        else:
            print('Invalid withdrawal amount!')

    def check_balance(self):
        print(f'Your current balance is : {self.balance} Taka')

    def check_transaction_history(self):
        print('Transaction history:')
        for trans in self.transaction:
            print(trans)

    def take_loan(self, amount):
        if Account.loan and Account.loan_count < 2:
            self.balance += amount
            Account.bank_balance -= amount
            Account.loan_count += 1
            print(f'You have taken a loan of {amount} Taka. New Balance : {self.balance} Taka.')
        elif Account.loan_count > 1:
            print('You cannot take more than one loan at a time.')
        else:
            print('Loan feature is currently off.')

    def transfer(self, receiver_acc, amount):
        if receiver_acc in Account.accounts:
            if self.balance >= amount:
                self.balance -= amount
                receiver_acc.balance += amount
                print(f'Transferred {amount} Taka to {receiver_acc.name}.')
            else:
                print('Insufficient balance for transfer!')
        else:
            print('Account does not exist.')

    @abstractmethod
    def show_info(self):
        pass

class User(Account):
    def __init__(self, name, email, address, acc_type, password) -> None:
        super().__init__(name, email, address, acc_type)
        self.password = password

    def show_info(self):
        print(f'Name : {self.name}')
        print(f'Email : {self.email}')
        print(f'Address : {self.address}')
        print(f'Account Type : {self.acc_type}')
        print(f'Account Number : {self.acc_num}')
        print(f'Balance : {self.balance}')

class Admin(Account):
    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = str(password)

    def delete_acc(self, account):
        if account in Account.accounts:
            Account.accounts.remove(account)
            print('Account has been removed.')
        else:
            print('Account does not exist')

    def see_all_accounts(self):
        for account in Account.accounts:
            account.show_info()

    def check_total_balance(self):
        print(f'Total balance of the bank is : {Account.bank_balance} Taka.')

    def check_total_loan(self):
        print(f'Total loan amount is : {sum(user.balance for user in Account.accounts if user.balance < 0)}')

    def on_off_loan(self, toggle):
        Account.loan = toggle
        if toggle:
            print('Loan feature is on.')
        else:
            print('Loan feature is off now.')

    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, address, password) -> None:
        super().__init__(name, email, address, 'Savings')
        self.password = password

    def show_info(self):
        return super().show_info()
    
class CurrentAccount(Account):
    def __init__(self, name, email, address, password) -> None:
        super().__init__(name, email, address, 'Current')
        self.password = password

    def show_info(self):
        return super().show_info()
    
# Replica

admin = Admin('Admin', 'admin@gmail.com', '1234')
currentUser = None

while True:
    if currentUser is None:
        print('No user logged in!\n')
        ch = input('1. Register or 2. Login : ')

        if ch == '1':
            name = input('Name : ')
            email = input('Email : ')
            address = input('Address : ')
            acc_type = input('1. Savings or 2. Current Account : ')
            password = input('Pasword : ')

            if acc_type == '1':
                currentUser = SavingsAccount(name, email, address, password)
            elif acc_type == '2':
                currentUser = CurrentAccount(name, email, address, password)
            else:
                print('Invalid account type. Try again.')
        elif ch == '2':
            email = input('Email : ')
            password = input('Password : ')

            if email == admin.email and password == admin.password:
                currentUser = admin
                print('\nWelcome Admin!\n')
            else:
                valid_user = False
                for acc in Account.accounts:
                    if acc.email == email and acc.password == password:
                        currentUser = acc
                        valid_user = True
                        print(f'\nWelcome {currentUser.name}!\n')
                        break
                if not valid_user:
                    print('Invalid email or password. Try again.')

    else:
        print(f'\nWelcome {currentUser.name}!\n')
        if currentUser == Admin:
            print('1. Create an account')
            print('2. Delete a user account')
            print('3. See all user accounts list')
            print('4. Check the total available balance of the bank')
            print('5. Check the total loan amount')
            print('6. On or Off the loan feature of the bank')
            print('7. Logout')

            ch2 = input('\nEnter : ')
            if ch2 == '1':
                name = input('Name : ')
                email = input('Email : ')
                address = input('Address : ')
                acc_type = input('1. Savings or 2. Current Account : ')
                password = input('Pasword : ')

                if acc_type == '1':
                    currentUser = SavingsAccount(name, email, address, password)
                elif acc_type == '2':
                    currentUser = CurrentAccount(name, email, address, password)
                else:
                    print('Invalid account type. Try again.')
            elif ch2 == '2':
                acc_num = int(input('Enter the Account number to delete : '))
                acc_delete = None
                for account in Account.accounts:
                    if account.acc_num == acc_num:
                        acc_delete = account
                        break
                if acc_delete:
                    currentUser.delete_acc(acc_delete)
                else:
                    print('Account does not exist.')
            elif ch2 == '3':
                currentUser.see_all_accounts()
            elif ch2 == '4':
                currentUser.check_total_balance()
            elif ch2 == '5':
                currentUser.check_total_loan()
            elif ch2 == '6':
                toggle = input('Enter 1. ON to turn on loan feature, 2. OFF to turn off loan feature : ')
                if toggle == '1':
                    currentUser.on_off_loan(True)
                elif toggle == '2':
                    currentUser.on_off_loan(False)
                else:
                    print('Invalid input. Try again.')
            elif ch2 == '7':
                currentUser = None
                print('Logged out!')
            else:
                print('Invalid input. Try again.')

        else:
            print('1. Deposit')
            print('2. Withdraw')
            print('3. Check Balance')
            print('4. Check Transaction History')
            print('5. Take Loan')
            print('6. Transfer Amount')
            print('7. Logout')

            ch3 = input('\nEnter : ')
            if ch3 == '1':
                amount = int(input('Enter the amount to deposit : '))
                currentUser.deposit(amount)
            elif ch3 == '2':
                amount = int(input('Enter the amount to withdraw : '))
                currentUser.withdraw(amount)
            elif ch3 == '3':
                currentUser.check_balance()
            elif ch3 == '4':
                currentUser.check_transaction_history()
            elif ch3 == '5':
                amount = int(input('Enter the amount for the loan : '))
                currentUser.take_loan(amount)
            elif ch3 == '6':
                acc_num = int(input('Enter the account number : '))
                amount = int(input('Enter the amount to transfer : '))
                receiver_acc = None
                for account in Account.accounts:
                    if account.acc_num == acc_num:
                        receiver_acc = account
                        break
                if receiver_acc:
                    currentUser.transfer(receiver_acc, amount)
                else:
                    print('Account does not exist')
            elif ch3 == '7':
                currentUser = None
                print('Logged out!')
            else:
                print('Invalid input. Try again.')