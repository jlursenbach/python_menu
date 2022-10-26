#!/usr/bin/env python3
# Jacob Ursenbach
# 2022-07-21
# jlursenbach@csu.fullerton.edu
# @jlursenbach
#
#

"""
A default menu class
Allows menu items to be set and called
provides string for header etc
functions can have parameters
"""


class Menu(dict):
    """
    Menu is a dict
    """

    def __init__(self, name=None, header=None, body=None, footer=None, prompt="Please select a menu item: "):
        super().__init__()
        self.name = name
        self.border = "- " * 30
        self.header = header
        self.body = body
        self.footer = footer
        self.prompt = prompt

    @staticmethod
    def quit_program() -> None:
        """
        used to quit the program,
        (selecting q in menu calls this and breaks the menu loop)
        prints "< Exiting Menu"
        :return: None
        """
        print("< Exiting Menu")

    # this isn't really NEEDED? < (I never call this function,
    # but it can help another coder understand/use the menu)
    # this CAN be used in loops, and to add items to menu. Needed?
    @staticmethod
    def create_menu_tuple(
        function, parameters, menu_text, display_item
    ) -> tuple:
        """
        this is not currently being used int the program.
        used to provide a structured way to create new menus that reminds coders how they're built.
        :param function: name of the function to be called
        :param parameters: parameters for any function what needs them.
        :param menu_text: The text the user sees when printing the menu
        :param display_item: Bool - choose whether the item is printed or not
                allows additional user controls without needing a bloated menu
        :return: a tuple containing all of the above info
        """
        return function, parameters, menu_text, display_item

    # same as above
    @staticmethod
    def new_menu_item(menu_key: str, menu_tuple: tuple) -> dict:
        """
        adds a new menu item with the correct parameters to a menu.
        can call create_menu_tuple, or just put a tuple directly into the menu_tuple parameter
        :param menu_key: a string holding the text used to select a menu item
        :param menu_tuple: a tuple containing all the information in a menu
                (the tuple is better described in create_menu_tuple() function)
        :return: a dictionary object with a single key, and corresponding menu tuple
        """

        # a dict containing a single key, with a tuple containing
        # (function, parameters, "menu_text", display_item: bool, print_after: bool)
        menu_item = {menu_key: menu_tuple}
        return menu_item

    @staticmethod
    def print_strlist(str_list):
        """
        cheks if its a string or list
        if its a list of strings prints 1 line at a time
        :param str_list: list[str] or str
        :return: None
        """
        if isinstance(str_list, str):
            print(str_list)
        elif isinstance(str_list, list):
            for line in str_list:
                print(line)

    def print_menu(self) -> None:
        """
        prints the menu_text part of the tuple in the provided menu
                menu item format: {key: (function, parameters, "display text", bool(print item?)
        :return: None
        """
        # border = "- " * 30
        # print(f"{self.border}")

        self.print_strlist(self.header)
        self.print_strlist(self.body)

        print("\nPlease select a menu key from below: ")
        # print(self.border)

        # value[3] is a boolean value called 'display_item' stating whether to print menu item,
        # value[2] is the menu text the user will see printed
        # key is the dictionary key the user uses to select the menu item.
        for key, value in self.items():
            if value[3]:
                print(f"{key}: {value[2]}")
        # print(self.border)

        self.print_strlist(self.footer)

    def run_menu(self, print_statement=None) -> False:
        """
        Takes user input to choose a menu object, than runs the correlated menu function
        If an invalid entry is given, prints a warning to user, with reminders
        of how to quit or print the menu
        :return: BOOL value: False (once q is presses escapes menu,
         tells program menu is not running)
        """

        #  sentinel, priming loop
        choice = ''
        self.print_menu()
        # Q escapes menu and quits.
        while choice.upper() != 'Q':
            try:
                if print_statement:
                    print(print_statement)
                print(f"\n__{self.name}__: 'M' to print menu")
                choice = input(self.prompt).upper().strip()
                # menu_choice[0] is a function call,
                # menu_choice[1] holds the function parameters
                if self[choice][1] == ():
                    pr_bool = self[choice][0]()
                else:
                    # ToDo add *kwarg to call fucntion with multiple parameters
                    pr_bool = self[choice][0](self[choice][1])
                if self[choice][4] or pr_bool:
                    self.print_menu()

            # invalid entry provides user with a reminder.
            except LookupError:
                print(
                    '\nInvalid Entry. \n'
                    '                 M to print menu\n'
                    '                 Q to quit menu\n'
                )
        return False


if __name__ == '__main__':
    pass
