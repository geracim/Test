import os

shopping_list = []

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_help():
    clear_screen()
    print("What should we pick up at the store?")
    print("""
Enter 'done' to stop adding items.
Enter 'help' for this help.
Enter 'show' to see your current list.
Enter 'remove' to remove an item from your list.
""")

def add_to_list(item):
    show_list()
    if len(shopping_list):
        position = input("where should I add {}?\n"
            "Press Enter to add to the end of the list\n"
            "> ".format(item))
    else:
        position = 0
    try:
        position = abs(int(position))
    except ValueError:
        position = None
    if position is not None:
        shopping_list.insert(position - 1, item)
    else:
        shopping_list.append(new_item)

    print("Added! List has {} items.".format(len(shopping_list)))


def show_list():
    clear_screen()

    print("Here's your list:")

    index = 1
    for item in shopping_list:
        print("{}. {}".format(index, item))
        index += 1

    print('~' * 10)


show_help()

while True:
    new_item = input("> ")

    if new_item.upper() == 'DONE' or new_item.upper() == "QUIT":
        break
    elif new_item.upper() == 'HELP':
        show_help()
        continue
    elif new_item.upper() == 'SHOW':
        show_list()
        continue

    add_to_list(new_item)

show_list()