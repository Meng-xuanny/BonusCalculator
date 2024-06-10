from common import Total_ALLOWANCE


# this function is to make sure the user doesn't enter negative number of members
# or number larger than 5(maximum member number)
def validateNumberOfMembers():
    numberOfMembers = int(input('Enter the number of people in your team: '))

    # Validate the input
    while numberOfMembers < 1 or numberOfMembers > 5:
        if numberOfMembers < 1:
            print("The team has to have at least 1 member.")
        else:
            print("Number of members can't be more than 5.")
        numberOfMembers = int(input('Enter the number of people in your team: '))

    return numberOfMembers


# this function is to make sure the user doesn't enter negative balance or balance larger than total allowance
def validateBalance():
    balance = float(input('Please enter the balance for your team account: '))

    # input validation
    while balance > Total_ALLOWANCE or balance < 0:
        if balance > Total_ALLOWANCE:
            print(f"The balance cannot be larger than {Total_ALLOWANCE}.")

        else:
            print("Balance can't be negative.")

        balance = float(input('Please enter the balance for your team account: '))

    return balance


# this function is to make sure the user doesn't enter invalid amount spent
def validateAllowance(balance, allowance, position):
    allowanceSpent = float(input(f'Please enter the amount the {position} has spent: '))

    while allowanceSpent > allowance or allowanceSpent > balance or allowanceSpent < 0:
        if allowanceSpent > allowance:
            print(f'The number cannot be larger than {position} allowance: ${allowance}!')

        elif allowanceSpent > balance:
            print(f"The number can't exceed available balance ${balance}!")

        else:
            print('The amount cannot be negative.')

        allowanceSpent = float(input(f'Please enter the amount the {position} has spent: '))

    return allowanceSpent
