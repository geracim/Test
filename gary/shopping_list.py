# make a list to hold onto items
shopping_list = []
menu_choice = 0

# insert the block of functions below.
def show_menu():
    # display main menu
    print("""
Please type 1 to begin new list.
Type 2 to see current list.
Type 3 to close app.""")

def list_instructions():
    # print out instructions on how to use the app
    print("""
Enter an item and press [Ent] to save it.
Press [Ent] 2x to save list.""")

def show_list():
    # print out the list
    print("Here's your list: ")
    for item in shopping_list:
        print(item)

def add_to_list(new_item):
    # add new items to our list
    shopping_list.append(new_item)
    # print("Added {}. There are now {} things in list.".format(new_item, len(shopping_list)))

# Warning, there be while loops beyond this point.
# this is the first, and outer while loop which
# encompasses the shopping list & displays it.
while menu_choice == 0:
    show_menu()
    try:
        menu_choice = input("Your choice: ")
    except NameError:
        print("That's not a number!")
            
    else:
        continue
# this is the inner while loop which asks users for
# input for shopping list & adds each entry to list
    while menu_choice != 0:
        if menu_choice == 3:
            menu_choice = 0
            continue
        elif menu_choice == 2:
            show_list()
            menu_choice = 0
            continue
        elif menu_choice == 1:
            new_item = input(str(len(shopping_list)+ 1) + ". ")
            if new_item == "":
                menu_choice = 0
                break
            else:
                add_to_list(new_item)
            continue
