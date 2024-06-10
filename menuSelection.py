from calculator import calculateAllowance, calculateBonus
from functions import createAccount, exitProgram, validateTeam
from printer import printAllowance, printResult


# calling functions in accordance to user selection
def selectOption(userInput):

    if userInput == 'A' or userInput == 'a':
        createAccount()
        return

    elif userInput == 'B' or userInput == 'b':
        printAllowance()
        return

    elif userInput == 'C' or userInput == 'c':
        balance, result = calculateAllowance()
        printResult(result)
        return

    elif userInput == 'D' or userInput == 'd':
        printAllowance()
        bonus,result = calculateBonus()
        printResult(result)
        printResult(f"The bonus this team is going to receive is ${bonus:.2f} based on the current balance.\n")
        return

    else:
        exitProgram()

