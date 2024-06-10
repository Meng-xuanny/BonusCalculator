import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring, askinteger, askfloat
from calculator import calculateRemainingBalance, calculateTotalAvailableAllowance, \
    calculateAverageAvailableAllowance, calculateRate
from common import ALLOWANCE_FOR_SUPERVISOR, ALLOWANCE_FOR_TEAM_MEMBER
from utils import formatRemainingAllowance


class BonusGUI:

    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Bonus Calculator")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure the style for the buttons
        self.style.configure('Colored.TButton', relief=tk.FLAT, background='lightgreen', borderwidth=0, border=0)

        # Welcome message label with background color
        self.labelWelcome = tk.Label(self.root, text="Welcome to Bonus Calculator", font=("Arial", 16), bg="lightblue")
        self.labelWelcome.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Option menu label and dropdown
        self.labelOption = tk.Label(self.root, text="Select an option:")
        self.labelOption.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Variables
        self.options = ["A. Create Accounts", "B. View Member Allowances", "C. Calculate and View Personal Allowances",
                        "D. Calculate and View Bonus"]
        self.clicked = tk.StringVar()
        self.output = tk.StringVar()
        self.teamAccounts = {}

        # Initialize self.entry_widgets as an empty list
        self.entryWidgets = []

        self.clicked.set(self.options[0])

        self.optionMenu = tk.OptionMenu(self.root, self.clicked, *self.options)
        self.optionMenu.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        # Team number input
        self.labelTeam = tk.Label(self.root, text="Enter Team Number:")
        self.labelTeam.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.entryTeam = tk.Entry(self.root)
        self.entryTeam.grid(row=2, column=1, padx=10, pady=5)

        # Balance input
        self.labelBalance = tk.Label(self.root, text="Enter Balance:")
        self.labelBalance.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.entryBalance = tk.Entry(self.root)
        self.entryBalance.grid(row=3, column=1, padx=10, pady=5)

        # Execute button
        self.btnExecute = ttk.Button(self.root, text="Execute", command=self.selectOption, style='Colored.TButton')
        self.btnExecute.grid(row=4, column=0, pady=12, padx=15, ipadx=10, ipady=5, sticky="w")

        # Quit button
        self.btnQuit = ttk.Button(self.root, text='Exit', command=self.root.destroy, style='Colored.TButton')
        self.btnQuit.grid(row=4, column=1, pady=12, padx=15, ipadx=10, ipady=5, sticky="e")

        # Output
        self.entryOutput = tk.Entry(self.root, textvariable=self.output, state='readonly', bg='lightblue', width=100,
                                    bd=3)
        self.entryOutput.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipady=40, sticky="ew")

        # Read team data from file and display in self.entryOutput
        self.teamDataList = self.readFile()
        self.fileContent = self.displayFileData(self.teamDataList)
        self.displayResult(self.fileContent)

        tk.mainloop()

    def selectOption(self):
        # Clear the output field
        self.entryOutput.delete(0, tk.END)
        self.output.set('')

        selection = self.clicked.get()

        if selection == "A. Create Accounts":
            self.createAccount()

        elif selection == "B. View Member Allowances":
            self.showAllowance()

        elif selection == "C. Calculate and View Personal Allowances":
            self.calculateAllowance()

        else:
            self.showAllowance()
            bonus, result = self.calculateBonus()
            self.output.set(
                f"The bonus this team is going to receive is ${bonus:.2f} based on the current balance.\n")

    def createAccount(self):
        team = self.entryTeam.get()
        balance = self.entryBalance.get()

        if team == '' or balance == '':
            messagebox.showinfo('warning', "Your team number and balance can't be empty!")
            return

        self.teamAccounts[team] = balance
        messagebox.showinfo('Congrats!', f'Account {team} has been created!')

    def showAllowance(self):
        self.entryOutput.delete(0, tk.END)
        self.output.set(f'Allowance for each supervisor: ${ALLOWANCE_FOR_SUPERVISOR}. ' +
                        f'Allowance for each team member: ${ALLOWANCE_FOR_TEAM_MEMBER}.')

    def calculateAllowance(self):
        try:
            # Initialize variables
            totalSpent = 0.00
            resultStr = ''
            memberSpentList = []

            # Get team number and number of people on the team from user
            teamNumber = self.getTeamNumber()

            # Check if team exists
            if teamNumber not in self.teamAccounts:
                messagebox.showinfo('warning', "Team doesn't exist. Create an account first.")
                return

            numOfMember = self.getNumberOfMembers()
            balance = float(self.teamAccounts[teamNumber])

            # Get supervisor spending
            supervisorSpending = self.getSupervisorSpending(balance)

            # Calculate total spent and remaining balance
            totalSpent += supervisorSpending
            remainingBalance = calculateRemainingBalance(balance, supervisorSpending)

            # Generate result string
            resultStr += f'Starting balance for team account {teamNumber}: ${balance}\n'
            resultStr += f"Entered amount spent by the supervisor: ${supervisorSpending:.2f}\n"

            # Get member spending
            memberSpentList, memberResult = self.getMemberSpending(numOfMember, remainingBalance)

            # Update total spent and remaining balance
            totalSpent += sum(memberSpentList)
            remainingBalance -= sum(memberSpentList)

            # Generate result string for supervisor and members
            resultStr += memberResult
            resultStr += formatRemainingAllowance(supervisorSpending, memberSpentList)

            # Calculate total and average available allowance
            totalAvailableAllowance = calculateTotalAvailableAllowance(balance, totalSpent)
            average = calculateAverageAvailableAllowance(totalAvailableAllowance, numOfMember)

            resultStr += f"Total available allowance: ${totalAvailableAllowance:.2f}\n"
            resultStr += f"Average available allowance: ${average:.2f}"

            self.displayResult(resultStr)

            return totalAvailableAllowance, resultStr

        except Exception as e:
            print('An error has occurred:', e)

    @staticmethod
    def getTeamNumber():
        teamNumber = askstring("Team Number", "Enter Team Number:")
        return teamNumber

    @staticmethod
    def getNumberOfMembers():
        numOfMember = askinteger("Number of People", "Enter Number of People on the Team:")

        # Validate the input
        while numOfMember < 1 or numOfMember > 5:
            if numOfMember < 1:
                messagebox.showwarning('warning',"The team has to have at least 1 member.")
            else:
                messagebox.showwarning('warning',"Number of members can't be more than 5.")
            numOfMember = askinteger("Number of People", "Enter Number of People on the Team:")

        return numOfMember

    def getSupervisorSpending(self, balance):
        supervisorSpending = self.validateAllowance(balance, ALLOWANCE_FOR_SUPERVISOR, 'supervisor')
        return supervisorSpending

    def getMemberSpending(self, numOfMember, balance):
        memberSpentList = []
        resultStr = ''
        for counter in range(1, numOfMember):
            allowanceSpentByMember = self.validateAllowance(balance, ALLOWANCE_FOR_TEAM_MEMBER,
                                                            f'team member {counter}')
            memberSpentList.append(allowanceSpentByMember)
            resultStr += f"Entered amount spent by team member {counter}: ${allowanceSpentByMember:.2f}\n"
            balance -= allowanceSpentByMember
        return memberSpentList, resultStr

    @staticmethod
    def validateAllowance(balance, allowance, position):
        allowanceSpent = askfloat(f"{position} Spending", f"Enter the amount spent by the {position}:")

        while allowanceSpent > allowance or allowanceSpent > balance or allowanceSpent < 0:
            if allowanceSpent > allowance:
                messagebox.showwarning('warning', f'The number cannot be larger than {position} allowance: ${allowance}!')

            elif allowanceSpent > balance:
                messagebox.showwarning('warning', f"The number can't exceed available balance ${balance}!")

            else:
                messagebox.showwarning('warning', 'The amount cannot be negative.')

            allowanceSpent = askfloat(f"{position} Spending", f"Enter the amount spent by {position}:")

        return allowanceSpent

    def displayResult(self, result):
        # Clear existing entry widgets
        for entry in self.entryWidgets:
            entry.destroy()

        # Split the result string into separate lines
        result_lines = result.split('\n')

        # Create and display entry widgets for each line of the result
        for i, line in enumerate(result_lines):
            entry = tk.Entry(self.root, bg='lightblue', width=60, bd=3)
            entry.grid(row=6 + i, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            entry.insert(0, line)
            self.entryWidgets.append(entry)  # Store a reference to the entry widget

    def calculateBonus(self):
        balance, result = self.calculateAllowance()
        rate = calculateRate(balance)
        bonus = balance * rate

        return bonus, result

    @staticmethod
    def readFile():
        file = open("team_data.txt", 'r')
        teamDataList = file.readlines()
        file.close()
        return teamDataList

    def displayFileData(self, team):
        result = ''

        for line in team:
            data = line.strip().split(',')
            teamNumber = data[0]
            balance = float(data[1])
            numOfMembers = int(data[2])

            # Store file data in local variable teamAccounts
            self.teamAccounts[teamNumber] = balance

            result += f'Team number: {teamNumber}\n'
            result += f'Balance: ${balance}\n'
            result += f'Number of members: {numOfMembers}\n\n'

        return result
