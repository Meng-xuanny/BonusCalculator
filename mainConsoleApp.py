"""
Author: Mengxuan Liang
Date created: 13/04/2024
Date last changed: 21/04/2024
This program is a bonus calculator console application. It allows users to create accounts, view member allowances,
calculate and view personal allowances, and calculate and view bonuses for teams.
Users can input team numbers, balances, and spending information, and the program provides calculated results in the console.
Input: Team numbers, balances, spending information from the user through the console
Output: Calculated allowances, bonuses, and other relevant information displayed in the console
"""

from menu import displayMenu
from userInteraction import prompt


# main function
def main():
    print('--------------Bonus Calculator--------------\n')

    try:
        while True:
            displayMenu()
            userInput = input('Please enter the capital letter in front of the option: ')
            prompt(userInput)
            if userInput == 'e' or userInput == 'E':
                break
                
    except Exception as e:
        print(f'An error occurred: {e}. Please restart the app.')


if __name__ == '__main__':
    main()
