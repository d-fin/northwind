
def Menu():
    print("\n--------------------")
    print("1. Add a customer\n2. Add an order\n3. Remove an order")
    print("4. Ship an order\n5. Print pending orders (not shipped yet) with customer information")
    print("6. Restock products\n7. More options\n8. Exit")
    print("--------------------")
    x = int(input())

    return x

def MoreOptions():
    print("\n----------------------------------------")
    print("More options")
    print("1. Display all products")
    print("2. Display products by category")
    print("3. Display all customers by company name")
    print("4. Display employee info")
    print("5. Contact a supplier")
    print("7. Return to main menu")
    print("----------------------------------------")
    x = int(input())

    return x