from common import accountBalance, ALLOWANCE_FOR_SUPERVISOR, ALLOWANCE_FOR_TEAM_MEMBER
from utils import getTeamNumber, getNumberOfMembers, formatResultString, formatRemainingAllowance
from validator import validateAllowance


# this function is to calculate each team member's spending allowance, remaining allowance and total balance after
# spending
def calculateAllowance():
    try:
        # Get the team number, number of members and the account balance
        teamNumber = getTeamNumber()
        numberOfMembers = getNumberOfMembers()
        balance = accountBalance[teamNumber]

        # Calculate amount spent by the supervisor
        allowanceSpentBySupervisor = calculateSpending(balance, ALLOWANCE_FOR_SUPERVISOR, 'supervisor')
        remainingBalance = calculateRemainingBalance(balance, allowanceSpentBySupervisor)

        resultStr = formatResultString(teamNumber, balance, allowanceSpentBySupervisor)

        # Store the amount spent by supervisor in a running total and members spending in a list
        totalSpent = allowanceSpentBySupervisor
        memberSpentList = []

        # Loop through each team member and get their valid spending
        for counter in range(1, numberOfMembers):
            allowanceSpentByMember = calculateSpending(remainingBalance, ALLOWANCE_FOR_TEAM_MEMBER,
                                                       f'team member {counter}')
            memberSpentList.append(allowanceSpentByMember)
            totalSpent += allowanceSpentByMember
            remainingBalance -= allowanceSpentByMember
            resultStr += f"Entered amount spent by team member {counter}: ${allowanceSpentByMember:.2f}\n"

        resultStr += formatRemainingAllowance(allowanceSpentBySupervisor, memberSpentList)

        totalAvailableAllowance = calculateTotalAvailableAllowance(balance, totalSpent)
        average = calculateAverageAvailableAllowance(totalAvailableAllowance, numberOfMembers)

        resultStr += f"Total available allowance: ${totalAvailableAllowance:.2f}\n"
        resultStr += f"Average available allowance: ${average:.2f}\n"

        return totalAvailableAllowance, resultStr

    except Exception as e:
        print('An error has occurred:', e)


def calculateSpending(balance, allowance, member_type):
    allowanceSpent = validateAllowance(balance, allowance, member_type)
    return allowanceSpent


def calculateRemainingBalance(balance, allowanceSpentBySupervisor):
    remainingBalance = balance - allowanceSpentBySupervisor
    return remainingBalance


def calculateTotalAvailableAllowance(balance, totalSpent):
    totalAvailableAllowance = float(balance - totalSpent)
    return totalAvailableAllowance


def calculateAverageAvailableAllowance(totalAvailableAllowance, numberOfMembers):
    average = totalAvailableAllowance / numberOfMembers
    return average


# this function is to calculate the bonus rate based on the account balance
def calculateRate(balance):
    RATE_FOR_BALANCE_BELOW_50 = 0.05

    RATE_FOR_BALANCE_BETWEEN_50_AND_100 = 0.1

    RATE_FOR_BALANCE_BETWEEN_100_AND_200 = 0.25

    RATE_FOR_BALANCE_BETWEEN_200_AND_300 = 0.35

    RATE_FOR_BALANCE_ABOVE_300 = 0.5

    # Balance won't be negative because it's handled during input
    if balance < 50:
        rate = RATE_FOR_BALANCE_BELOW_50

    elif balance in range(50, 100):
        rate = RATE_FOR_BALANCE_BETWEEN_50_AND_100

    elif balance in range(100, 200):
        rate = RATE_FOR_BALANCE_BETWEEN_100_AND_200

    elif balance in range(200, 300):
        rate = RATE_FOR_BALANCE_BETWEEN_200_AND_300

    else:
        rate = RATE_FOR_BALANCE_ABOVE_300

    return rate


# this function is to calculate the bonus
def calculateBonus():
    balance, result = calculateAllowance()

    rate = calculateRate(balance)

    bonus = balance * rate

    return bonus, result
