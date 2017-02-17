def print_table(table, title_list, title, numeration=True):
    """
    Prints table with data

    Args:
        table (list of lists): table to display
        title_list (list): containing table headers
        title (str): containing title for table
        numeration (int): auto numerate table

    Returns:
        This function doesn't return anything it only prints to console.
    """
    print(title + "\n")
    if numeration:
        title_list.insert(0, "Id")
        for index, row in enumerate(table):
            row.insert(0, index+1)
    table.insert(0, title_list)
    for row_index, row in enumerate(table):
        for col_index, col in enumerate(row):
            if (type(col) == float) or (type(col) == int):
                table[row_index][col_index] = str(col) #str("{0:,.2f}".format(col))
    widths = [max(map(len, col)) for col in zip(*table)]
    sum_of_widths = sum(widths) + len(table[0]) * 3 - 1 # len(table[0]) - number of |
    for row in table:
        print("-" * sum_of_widths)
        print("|" + "  ".join((val.rjust(width) + "|" for val, width in zip(row, widths))))
    print("-" * sum_of_widths)


def print_menu(title, list_options, exit_message):
    """
    Displays a menu.

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        This function doesn't return anything it only prints to console.
    """
    print('\n'+title + ':')
    for i in range(len(list_options)):
        print('  ({}) {}'.format(i + 1, list_options[i]))
    print('  (0) ' + exit_message)


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.

    Args:
        list_labels (list): list of strings - labels of inputs
        title (str): title of the "input section"

    Returns:
        List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """

    inputs = []
    print(title)
    for item in list_labels:
        user_input = input(item + ': ').strip()
        inputs.append(user_input)
    return inputs


def print_error_message(message):
    """
    Displays an error message

    Args:
        message(str): error message to be displayed

    Returns:
        This function doesn't return anything it only prints to console.
    """

    print("Error:", message)


def handle_menu(menu_level="main"):
    """
    Displays a custom menu (menu_level).

    Args:
        menu_level (str): type of menu to display

    Returns:
        This function doesn't return anything it only prints to console.
    """

    if menu_level == "main":
        options = ["List statistics",
                   "Display 3 cities with longest names",
                   "Display county's name with the largest number of communities",
                   "Display locations, that belong to more than one category",
                   "Advanced search"]
        print_menu("\nWhat do you want to do?", options, "Exit program")
    elif menu_level == "add_shape":
        options = ["Circle",
                   "Rectangle",
                   "Square",
                   "Triangle",
                   "Equilateral triangle",
                   "Regular pentagon"]
        print_menu("\nChoose shape to add", options, "Return to main menu")
    elif menu_level == "show_formulas":
        options = ["Circle",
                   "Rectangle",
                   "Square",
                   "Triangle",
                   "Equilateral triangle",
                   "Regular pentagon"]
        print_menu("\nChoose shape to display formulas", options, "Return to main menu")
