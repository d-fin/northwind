'''
Below are my functions that create the query for the option chosen by the user.
query is returned to main and executed there. 
'''
from datetime import timedelta
import datetime
import pandas as pd 
import random as rand
from MoreOptionsFunctions import DisplayAllProducts

pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

def AddCustomer(cursor):
    def EnterInformation():
        try: 
            address = []
            temp, id = None, None

            companyName = input('Enter company name: ')
            contactName = input('Enter contact name (First and Last name): ')
            contactTitle = input('Enter title: ')
            
            companyName = companyName.title()
            contactName = contactName.title()
            contactTitle = contactTitle.title()

            temp = str(input('Enter street address: '))
            address.append(temp)
            temp = str(input('Enter city: '))
            address.append(temp)
            while True:
                try: temp = int(input('Enter postal code: '))
                except Exception as e: print("\nEnter a valid postal code!")
                else:
                    temp = str(temp) 
                    break 
            address.append(temp)
            temp = str(input('Enter country: '))
            address.append(temp)

            for i in range(len(address)):
                if i == 0:
                    temp = address[0].split(" ")
                    for j in range(len(temp)):
                        if j != 0: temp[j] = temp[j].title()
                    x = " ".join(temp)
                    address[i] = x 
                elif i == len(address) - 1: address[i] = address[i].upper()
                else: address[i] = address[i].title() 

            while True: 
                try: 
                    phone = str(input('Enter phone number: (numbers only) '))
                    fax = str(input('Enter fax number: (numbers only) '))
                    if len(phone) == 10 and len(fax) == 10 and phone.isdigit() == True and fax.isdigit() == True:
                        phone = '({}) {}-{}'.format(phone[:3], phone[3:6], phone[6:])
                        fax = '({}) {}-{}'.format(fax[:3], fax[3:6], fax[6:])
                        break 
                    else: raise Exception("\nEnter numbers only no characters!")
                except Exception as e: print(e)
                    
            copyCompName = companyName
            copyCompName = copyCompName.split(" ")
            if len(copyCompName) > 1:
                id = copyCompName[0][:3] + copyCompName[1][:2]
            else: 
                id = copyCompName[0][:5]
            id = id.upper()
        except Exception as e:
            print(e)
        else: return id, companyName, contactName, contactTitle, address, phone, fax

    
    while True: 
        try: 
            id, companyName, contactName, contactTitle, address, phone, fax = EnterInformation()
            print("\n")
            print("-" * (len(" ".join(address)) + 10))
            print(f'Customer ID - {id}\nCompany Name - {companyName}\nContact name/title - {contactName} : {contactTitle}')
            print(f'Address - {" ".join(address)}\nPhone # - {phone}\nFax # - {fax}')
            print("-" *  (len(" ".join(address)) + 10))
            print(f'\nIs the above information correct? (Press 1 to continue or 0 to restart.) ')
            x = 0
            while True: 
                try: 
                    x = int(input())
                    if x > 1 or x < 0: raise Exception("\nEnter a valid option.")
                except Exception as e: print(e)
                else: break 
        except Exception as e: print(e)
        else: 
            if x == 0: pass 
            else: break 

    q1 = 'INSERT INTO Customers (CustomerID, CompanyName, ContactName, ContactTitle, Address, City, PostalCode, Country, Phone, Fax)'
    q2 = f'VALUES("{id}", "{companyName.title()}", "{contactName.title()}", "{contactTitle.title()}", "{address[0]}", "{address[1]}", "{address[2]}", "{address[3]}", "{phone}", "{fax}");'    
    return q1 + '\n' + q2
    
def AddOrder(cursor):
    order = []
    while True: 
        try: 
            print(f'\n1. Enter product ID\'s: \n2. Display product list: \n3. Submit order. ')
            option = int(input())
        except: print(f'\n{option} is not valid. Please enter a valid option.')
        else:
            if option == 1: 
                try: 
                    while True: 
                        id = input("\nEnter product ID: (Enter 0 to quit) ")
                        if int(id) == 0: break 
                        else:  
                            cursor.execute(f'SELECT * FROM products WHERE ProductID={id}')
                            row = cursor.fetchone()
                            if row == None: 
                                raise Exception("\nProduct ID does not exist.\n")
                            else: 
                                if row[9] != 'n': 
                                    print(f'\n{row[1]} is discontinued.\n')
                                else:
                                    tempQuery = f'SELECT ProductName, QuantityPerUnit, UnitPrice, UnitsInStock FROM products WHERE ProductID={id};'
                                    cursor.execute(tempQuery)
                                    df = pd.DataFrame(cursor.fetchall(), columns=['Product', 'Quantity/Unit', 'Price', 'Stock'])
                                    print(f'\n{df.to_string(index=False)}\n')
                                   
                                    while True: 
                                        quantity = int(input("Enter quantity: "))
                                        if quantity == 0: 
                                            print(f'\nProduct - {row[1]} - will not be added to the order.')
                                            break 
                                        elif quantity > row[6]:
                                            print(f'{row[1]} only has {row[6]} in stock. Please select a lesser amount or 0 to cancel')
                                        else: 
                                            temp = [id, quantity]
                                            order.append(temp)
                                            break 
                except Exception as e:
                    print(e)
            elif option == 2:
                DisplayAllProducts(cursor)
            elif option == 3: 
                try: 
                    # generate new order id 
                    cursor.execute('SELECT MAX(OrderID) FROM orders;')
                    row = cursor.fetchone()
                    newID = int(row[0]) + 1

                    # get customer/order/order_detail info 
                    while True: 
                        customerID = input("\nEnter the customers ID: ")
                        customerID = customerID.upper()
                        x = f'SELECT CompanyName, ContactName, Address FROM customers WHERE CustomerID=\'{customerID}\';'
                        cursor.execute(x)
                        row = cursor.fetchone()
                        if row == None: print(f'A customer with the id - {customerID} does not exist.')
                        else: 
                            print(f'\nCompany Name : {row[0]}\nContact Name : {row[1]}\nAddress : {row[2]}')
                            cont = input("\nIf the above customer data is correct and you wish to continue enter 1 or 0 to cancel: ")
                            if int(cont) == 1: 
                                break 
                
                except Exception as e: 
                    print(e)
                    return False, False, False 

                else:
                    y = f'SELECT CompanyName, Address, City, Region, PostalCode, Country FROM customers WHERE CustomerID=\'{customerID}\';'
                    cursor.execute(y)
                    customerData = cursor.fetchone()

                    unitPrices = []
                    shippingCost = 0.00

                    for i in order: 
                        discount = 0
                        q = f'SELECT UnitPrice, ReorderLevel FROM products WHERE ProductID={i[0]};'
                        cursor.execute(q)
                        unitPrice = cursor.fetchone()
                        discount = ( round(float(unitPrice[1] / 100), 2) )
                        temp = [i[0], i[1], unitPrice[0], discount]
                        shippingCost += float(unitPrice[0]) * int(i[1])
                        unitPrices.append(temp)
                                        
                    today = datetime.datetime.today()
                    requiredDate = today + timedelta(days=90)
                    today = today.strftime("%Y-%m-%d %H:%M:%S")
                    requiredDate = requiredDate.strftime("%Y-%m-%d %H:%M:%S")
                    shippedVia = rand.randint(1, 3)
                    shippingCost = round((shippingCost * .1), 2)

                    query = f'SELECT EmployeeID FROM employees WHERE Title=\'Sales Representative\';'
                    cursor.execute(query)
                    eids = [x[0] for x in cursor.fetchall()]
                    eid = eids[rand.randint(0, (len(eids) - 1))]

                    query = f'SELECT CompanyName, Phone FROM shippers WHERE ShipperID={shippedVia};'
                    cursor.execute(query)
                    df = pd.DataFrame(cursor.fetchall(), columns=['Name', 'Phone #'])
                    print(f'\nThe order will be shipped via the shipping company listed below.\n\n{df.to_string(index=False)}')
                    print(f'\nShipping Costs (10% of total cost) = ${shippingCost:.2f}')
                    input("\nPress Enter to continue...")

                    # make queries 
                    order_detail_queries = []
                    for i in unitPrices: 
                        order_detailsQ = f'INSERT INTO order_details (OrderID, ProductID, UnitPrice, Quantity, Discount)\n'
                        order_detailsQ2 = f'VALUES({newID}, {i[0]}, {i[2]}, {i[1]}, {i[3]});'
                        order_detail_queries.append(order_detailsQ + order_detailsQ2)
                        

                    orderQ1 = f'INSERT INTO orders (OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipPostalCode, ShipCountry)\n'
                    orderQ2 = f'VALUES({newID}, \'{customerID}\', {eid}, \'{today}\', \'{requiredDate}\', NULL, {shippedVia}, {shippingCost}, \"{customerData[0]}\", \'{customerData[1]}\', \'{customerData[2]}\', \'{customerData[4]}\', \'{customerData[5]}\');'
                    orderQuery = orderQ1 + orderQ2

                    productQueries = []
                    for i in order:
                        temp = f'UPDATE products SET UnitsInStock=UnitsInStock-{i[1]} WHERE ProductID={i[0]};'
                        productQueries.append(temp)

                    return order_detail_queries, orderQuery, productQueries
                    
def RemoveOrder(cursor):
    try:
        cursor.execute('SELECT OrderID, CustomerID FROM orders WHERE ShippedDate IS NULL;')
        df = pd.DataFrame(cursor.fetchall(), columns=['OID', 'CID'])
        print(f'\n{df.to_string(index=False)}')

        while True: 
            orderID = input("\nEnter order ID number: ")
            if orderID.isdigit() == True:
                cursor.execute(f'SELECT * FROM orders WHERE OrderID={orderID};')
                row = cursor.fetchone()

                if row == None: print("\nOrder ID does not exist.\n")
                else: break 

            else: print("\nEnter a valid order ID number.\n")

    except Exception as e: 
        print(e)
        return False, False
    else:
        try: 
            DisplayOrderDetails(cursor, orderID)
            print("\nAre you sure you want to cancel the above order? (Enter YES to cancel or NO to return to main menu.)")
            while True: 
                cancel = str(input())
                cancel = cancel.upper()
                if cancel == 'Y' or cancel == 'YES' or 'Y' in cancel: break 
                else: return False, False

        except Exception as e: print(e)
        else: 
            ordersQ = f'DELETE FROM orders WHERE OrderID={orderID};'
            order_detailsQ = f'DELETE FROM order_details WHERE OrderID={orderID};'
            return ordersQ, order_detailsQ
     

def ShipOrder(cursor):
    try:
        query = f'SELECT OrderID, CustomerID, EmployeeID, OrderDate FROM orders WHERE ShippedDate IS NULL;'
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=['OID', 'CID', 'EID', 'Order Date'])
        print("\n")
        print(df.to_string(index=False))

    except Exception as e: print(e)

    else: 
        try: 
            while True: 
                print(f'\nEnter order ID for order being shipped today: (or 0 to quit)')
                id = int(input())

                if id == 0: return False 

                exists = False 
                query = f'SELECT ShippedDate FROM orders WHERE OrderId={id};'
                cursor.execute(query)
                x = cursor.fetchone()
                if x[0] == None: exists = True
                

                if exists == False: 
                    print("\nID entered does not need to be shipped.")
                else: 
                    break 
                    
        except Exception as e: print(e)
        else:
            DisplayOrderDetails(cursor, id)
            print(f'\nThe above order will be shipped today.\nPress Enter to continue...')
            input()

            today = datetime.datetime.today()
            today = today.strftime("%Y-%m-%d %H:%M:%S")
            query = f'UPDATE orders SET ShippedDate=\'{today}\' WHERE OrderID={id};'
            return query 

def PrintPendingOrders(cursor):
    try: 
        cursor.execute("SELECT OrderId, CustomerID, ShipName, OrderDate FROM orders WHERE ShippedDate IS NULL ORDER BY OrderDate;")
        df = pd.DataFrame(cursor.fetchall(), columns=['OID', 'CID', 'Name', 'Order Date'])
    except Exception as e: 
        print(e)
        return False 
    else: 
        try: 
            cursor.execute("SELECT OrderID, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry FROM orders WHERE ShippedDate IS NULL ORDER BY OrderDate;")
        except Exception as e:
            print(e)
            return False 
        else: 
            data = cursor.fetchall()
            x = []
            for i in data: 
                temp = []
                temp.append(i[0])
                if i[3] == '': temp.append(f'{i[1]} {i[2]} {i[4]} {i[5]}')
                else: temp.append(f'{i[1]} {i[2]} {i[3]} {i[4]} {i[5]}')
                x.append(temp)

            df2 = pd.DataFrame(x, columns=['OID', 'Address'])
            result = df.merge(df2, on='OID', how='inner')
            print(result.to_string(index=False))

            return True 
    
def RestockProducts(cursor):
    while True:
        try:   
            print("1. Display all products: ")
            print("2. Enter product ID to restock: ")
            choice = int(input())
        except Exception as e:
            print(f'{e}\nEnter a valid option. ')
        
        else: 
            if choice == 1:
                DisplayAllProducts(cursor)
            else:
                while True: 
                    try:
                        id = int(input("Enter product ID for product to be restocked: "))
                        query = f'SELECT ProductID, ProductName, QuantityPerUnit, UnitsInStock, Discontinued FROM products WHERE ProductID={id};'
                        cursor.execute(query)
                        row = cursor.fetchone()
                        if row == None: raise Exception("\nProduct ID does not exist. ")
                        else:
                            if row[4] == 'n':
                                query = f'SELECT ProductID, ProductName, QuantityPerUnit, UnitsInStock, Discontinued FROM products WHERE ProductID={id};'
                                cursor.execute(query)
                                df = pd.DataFrame(cursor.fetchall(), columns=['PID', 'Name', 'Quantity/Unit', 'Current Stock', 'Discontinued'])
                                print("\n")
                                print(df.to_string(index=False))
                                restockQuantity = int(input("\nEnter quantity to be restocked: "))
                                query = f'UPDATE products SET UnitsInStock=UnitsInstock+{restockQuantity} WHERE ProductID={id};'
                                return query 
                            else: 
                                print("\nThis product is discontinued - No need to restock. ")
                                return False
                                
                    except Exception as e: 
                        print(f'{e}')
                        return False 



def DisplayOrderDetails(cursor, orderID):
    order_detail_query = f'SELECT OrderID, ProductID, UnitPrice, Quantity, Discount FROM order_details WHERE OrderID={orderID};'
    order_query = f'SELECT CustomerID, OrderDate, ShipName, ShipAddress, ShipCity, ShipPostalCode, ShipCountry FROM orders WHERE OrderID={orderID};'

    cursor.execute(order_detail_query)
    order_details = cursor.fetchall()

    x = []
    for i in order_details:
        query = f'SELECT ProductName, QuantityPerUnit FROM products WHERE ProductID={i[1]};'
        cursor.execute(query)
        product = cursor.fetchone()
        temp = [i[1], product[0], product[1], i[2], i[3], i[4]]
        x.append(temp)
    productDf = pd.DataFrame(x, columns=['PID', 'Product Name', 'Quantity/Unit', 'Price', 'Quantity', 'Discount'])

    cursor.execute(order_query)
    order = cursor.fetchone()

    address = [str(order[3]), str(order[4]), str(order[5]), str(order[6])]
    address = " ".join(address)
    order = [str(orderID), str(order[0]), str(order[2]), str(order[1].strftime("%Y-%m-%d")), address]
    orderDf = pd.DataFrame([order], columns=['CID', 'OID', 'Name', 'Order Date', 'Address'])

    print(f'\n{orderDf.to_string(index=False)}')
    print("-" * 100)
    print(f'{productDf.to_string(index=False)}')
    print("-" * 100)