# this function is to allow users to create a team account and enter balance
from common import accountBalance
from validator import validateBalance


# This function is to get user to add values into the accountBalance dictionary
def createAccount():
    shallContinue = True

    try:
        while shallContinue:
            team = input('Please enter your team number(integer): ')

            balance = validateBalance()

            accountBalance[team] = balance

            toContinue = input("Would you like to set up another account? Enter 'Y' or 'N': ")

            # input validation
            while toContinue != 'y' and toContinue != 'Y' and toContinue != 'n' and toContinue != 'N':
                print('Invalid Input.')
                toContinue = input("Would you like to set up another account? Enter 'Y' or 'N': ")

            if toContinue == 'n' or toContinue == 'N':
                shallContinue = False

        # print user-created accounts with balance
        for account in accountBalance:
            print(f"Balance for team account {account}: ${accountBalance[account]:.2f}")

        print() # Add a new line

    except ValueError:
        print("Please only enter numbers for balance.")
    except Exception as e:
        print(f'An error occurred: {e}. Please restart the app.')


# this function is to make sure the team the user entered is stored in the program,
# otherwise, prompt the user to create a team
def validateTeam():
    team = input('Please enter your team number you would like to access(integer): ')

    # input validation
    while team not in accountBalance:
        print("The account number you entered doesn't exit.")

        userChoice = input("Would you like to create an account? 'Y' or 'N': ")

        while userChoice != 'Y' and userChoice != 'y' and userChoice != 'N' and userChoice != 'n':
            print('Invalid input.')

            userChoice = input("Would you like to create an account? 'Y' or 'N': ")

        if userChoice == 'Y' or userChoice == 'y':
            createAccount()

        team = input('Please enter your team number you would like to access(integer): ')

    return team


# clear the object that stores user information and quit the program
def exitProgram():
    accountBalance.clear()

    print('Thank you for using the Bonus Calculator! See you next time!')
