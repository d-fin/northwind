'''
Below are my functions that execute the query for the option chosen by the user.
'''
from datetime import timedelta
import datetime
import pandas as pd 

pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

def AddCustomer(cursor):
    try: 
        address = []
        temp, id = None, None

        companyName = input('Enter company name: ')
        contactName = input('Enter contact name (First and Last name): ')
        contactTitle = input('Enter title: ')
        
        temp = str(input('Enter address: '))
        address.append(temp)
        temp = str(input('Enter city: '))
        address.append(temp)
        temp = str(input('Enter postal code: '))
        address.append(temp)
        temp = str(input('Enter Country: '))
        address.append(temp)
        phone = input('Enter phone number: ')
        fax = input('Enter fax number: ')

        copyCompName = companyName
        copyCompName = copyCompName.split(" ")
        if len(copyCompName) > 1:
            id = copyCompName[0][:3] + copyCompName[1][:2]
        else: 
            id = copyCompName[0][:5]
        id = id.upper()
        
        q1 = 'INSERT INTO Customers (CustomerID, CompanyName, ContactName, ContactTitle, Address, City, PostalCode, Country, Phone, Fax)'
        q2 = f'VALUES("{id}", "{companyName}", "{contactName}", "{contactTitle}", "{address[0]}", "{address[1]}", "{address[2]}", "{address[3]}", "{phone}", "{fax}");'
    
    except Exception as e:
        print(e)
        return False
    else:   
        return q1 + '\n' + q2
    
def AddOrder(cursor):
    order = []
    while True: 
        try: 
            print(f'\n1. Enter product ID\'s: \n2. Display product list: \n3. Submit order. ')
            option = int(input())
        except: print(f'{option} is not valid. Please enter a valid option.')
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
                                    print(f'\n{row[1]} is discontinued. Our apologies.\n')
                                else:
                                    tempQuery = f'SELECT ProductName, QuantityPerUnit, UnitPrice, UnitsInStock FROM products WHERE ProductID={id};'
                                    cursor.execute(tempQuery)
                                    df = pd.DataFrame(cursor.fetchall(), columns=['Product', 'Quantity/Unit', 'Price', 'Stock'])
                                    print(f'\n{df}\n')
                                   
                                    while True: 
                                        quantity = int(input("Enter quantity: "))
                                        if quantity == 0: 
                                            print(f'\nProduct - {row[1]} - will not be added to your order.')
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
                        customerID = input("\nEnter your customer ID number: ")
                        customerID = customerID.upper()
                        x = f'SELECT CompanyName, ContactName, Address FROM customers WHERE CustomerID=\'{customerID}\';'
                        cursor.execute(x)
                        row = cursor.fetchone()
                        if row == None: print(f'A customer with the id - {customerID} does not exist.')
                        else: 
                            print(f'\nCompany Name : {row[0]}\nContact Name : {row[1]}\nAddress : {row[2]}')
                            cont = input("\nIf this is you and you wish to continue enter 1 or 0 to cancel: ")
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
                    for i in order: 
                        q = f'SELECT UnitPrice FROM products WHERE ProductID={i[0]};'
                        cursor.execute(q)
                        unitPrice = cursor.fetchone()
                        temp = [i[0], i[1], unitPrice[0]]
                        unitPrices.append(temp)
                                        
                    today = datetime.datetime.today()
                    requiredDate = today + timedelta(days=90)
                    today = today.strftime("%Y-%m-%d %H:%M:%S")
                    requiredDate = requiredDate.strftime("%Y-%m-%d %H:%M:%S")

                    # make queries 
                    order_detail_queries = []
                    for i in unitPrices: 
                        order_detailsQ = f'INSERT INTO order_details (OrderID, ProductID, UnitPrice, Quantity, Discount)\n'
                        order_detailsQ2 = f'VALUES({newID}, {i[0]}, {i[2]}, {i[1]}, 0);'
                        order_detail_queries.append(order_detailsQ + order_detailsQ2)
                        

                    orderQ1 = f'INSERT INTO orders (OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipPostalCode, ShipCountry)\n'
                    orderQ2 = f'VALUES({newID}, \'{customerID}\', 1, \'{today}\', \'{requiredDate}\', NULL, 1, 1, \"{customerData[0]}\", \'{customerData[1]}\', \'{customerData[2]}\', \'{customerData[4]}\', \'{customerData[5]}\');'
                    orderQuery = orderQ1 + orderQ2

                    productQueries = []
                    for i in order:
                        temp = f'UPDATE products SET UnitsInStock=UnitsInStock-{i[1]} WHERE ProductID={i[0]};'
                        productQueries.append(temp)

                    return order_detail_queries, orderQuery, productQueries
                    
def RemoveOrder(cursor):
    try:
        while True: 
            orderID = input("Enter order ID number: ")
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
        ordersQ = f'DELETE FROM orders WHERE OrderID={orderID};'
        order_detailsQ = f'DELETE FROM order_details WHERE OrderID={orderID};'
        return ordersQ, order_detailsQ
     

def ShipOrder(cursor):
    return 

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
            print(result)

            return True 
    
def RestockParts(cursor):
    return

def DisplayAllProducts(cursor):
    try: 
        cursor.execute("SELECT DISTINCT ProductID, ProductName, SupplierID, QuantityPerUnit, UnitPrice FROM products;")
        df = pd.DataFrame(cursor.fetchall(), columns=['PID', 'Product Name', 'SID', 'Quant/Unit', 'Price'])
        cursor.execute("SELECT DISTINCT SupplierID, CompanyName FROM suppliers;")
        df2 = pd.DataFrame(cursor.fetchall(), columns=['SID', 'Supplier Name'])
    except Exception as e: 
        print(e)
        return False 
    else: 
        result = df.merge(df2, on='SID')
        result.drop(columns='SID', axis=1, inplace=True)
        print(result)
    
    

def DisplayCustByCompName(cursor):
    return 