from common import ALLOWANCE_FOR_SUPERVISOR, ALLOWANCE_FOR_TEAM_MEMBER
from functions import validateTeam
from validator import validateNumberOfMembers


def getTeamNumber():
    teamNumber = validateTeam()
    return teamNumber


def getNumberOfMembers():
    numberOfMembers = validateNumberOfMembers()
    return numberOfMembers


def formatResultString(teamNumber, balance, allowanceSpentBySupervisor):
    resultStr = ''
    resultStr += '\n--------------------result--------------------\n'
    resultStr += f'Starting balance for team account {teamNumber}: ${balance}\n'
    resultStr += f"Entered amount spent by the supervisor: ${allowanceSpentBySupervisor:.2f}\n"
    return resultStr


def formatRemainingAllowance(allowanceSpentBySupervisor, memberSpentList):
    resultStr = f"\nAvailable allowance for the supervisor: ${str(ALLOWANCE_FOR_SUPERVISOR - allowanceSpentBySupervisor)}\n"
    counter = 1
    for amount in memberSpentList:
        resultStr += f"Available allowance for the team member {counter}: ${(ALLOWANCE_FOR_TEAM_MEMBER - amount):.2f}\n"
        counter += 1
    return resultStr
