from menuSelection import selectOption


# prompt the user to select options on the menu
def prompt(userInput):

    while (userInput != 'A' and userInput != 'a' and userInput != 'B' and userInput != 'b' and userInput != 'C'
           and userInput != 'c' and userInput != 'D' and userInput != 'd' and userInput != 'E' and userInput != 'e'):
        print('Invalid input. Please only select A, B, C, D, or E')

        userInput = input('Please enter the capital letter in front of the option: ')

    selectOption(userInput)

    return


