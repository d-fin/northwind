
def Menu():
    print("\n--------------------")
    print("1. add a customer\n2. add an order\n3. remove an order")
    print("4. ship an order\n5. print pending orders (not shipped yet) with customer information")
    print("6. restock parts\n7. more options\n8. exit")
    print("--------------------")
    x = int(input())

    return x

def MoreOptions():
    print("\n----------------------------------------")
    print("More options")
    print("1. display all products")
    print("2. display all customers by company name")
    print("7. return to main menu")
    print("----------------------------------------")
    x = int(input())

    return x