'''
David Finley 
DBMS Assignment 4 - Northwind 
'''
import mysql.connector as dbconn

from UI import *
from MainMenuFunctions import * 
from MoreOptionsFunctions import * 

def main():
    def commit(query):
        try: 
            cursor.execute('START TRANSACTION') 
            cursor.execute(query)
            db.commit()
        except Exception as e:
            print(e)
            return False 
        else: return True 

    try:
        db = dbconn.connect(host="localhost", user="cs4430", passwd="cs4430", db="northwind")
        cursor = db.cursor()
    except Exception as e:
        print(f'{e}\nCould not connect to database')
        exit(0)
    else: 
        try: 
            while True: 
                choice, query = 0, None 
                choice = Menu()

                if choice == 1: 
                    query = AddCustomer(cursor)
                    if query == False: pass 
                    else:
                        if commit(query) == True: print(f'\nCustomer has been added.')
                        else: print(f'\nFailed to add customer.')

                elif choice == 2: 
                    order_detail_query, order_query, product_queries = AddOrder(cursor)
                    if order_detail_query == False or order_query == False or product_queries == False:
                        print(f'\nThere was an error submitting the order.')
                    else: 
                        try: 
                            cursor.execute('START TRANSACTION')
                            cursor.execute(order_query)
                            for i in order_detail_query:
                                cursor.execute(i)
                            for i in product_queries:
                                cursor.execute(i)
                            db.commit()
                        except Exception as e:
                            print(f'{e}\nCannot submit order.')
                        else: 
                            print("\nSuccessfully submitted order!")
                            print("\n1. Generate invoice.\n2. Return to main menu")
                            try: 
                                while True: 
                                    x = input()
                                    if x.isdigit == False: 
                                        raise Exception("Enter an integer")
                                    if int(x) > 2 or int(x) < 1:
                                        raise Exception("\nEnter a valid choice.\n") 
                                    else: 
                                        GenerateInvoice(cursor)
                                        break 
                            except Exception as e: print(e)
                           
                elif choice == 3:
                    orderQuery, orderDetailQuery = RemoveOrder(cursor) 
                    if orderQuery == None or orderDetailQuery == None or orderDetailQuery == False or orderQuery == False: 
                        print("\nOrder will not be removed.")
                    else:
                        try: 
                            cursor.execute('START TRANSACTION')
                            cursor.execute(orderDetailQuery)
                            cursor.execute(orderQuery)
                            db.commit()
                        except Exception as e: 
                            print(e)
                            print("\nCannot remove order.")
                        else: print(f'\nOrder removed!')
                
                elif choice == 4:
                    query = ShipOrder(cursor)
                    if query == False: pass 
                    else: 
                        if commit(query) == True: print("\nSuccessfully shipped order!")
                        else: print("\nFailed to send order to shipping. ")

                elif choice == 5:
                    query = PrintPendingOrders(cursor)
                    if query == True: pass 
                    else: print("\nThere was an error displaying the pending orders.")
                
                elif choice == 6: 
                    query = RestockProducts(cursor)
                    if query == False: pass 
                    else:
                        if commit(query) == True: print("\nSuccessfully updated the inventory!")
                        else: print("\nFailed to update inventory. ")

                elif choice == 7:
                    choice = MoreOptions()
                    if choice == 1: 
                        DisplayAllProducts(cursor)
                    elif choice == 2:
                        DisplayProductsByCategories(cursor)
                    elif choice == 3:
                        DisplayCustByCompName(cursor)
                    elif choice == 4: 
                        DisplayEmployeeInfo(cursor)
                    elif choice == 5:
                        ContactSupplier(cursor)

                elif choice == 8:
                    break 
        except Exception as e:
            print(e)
        finally:
            db.rollback()
            db.close()
            print("Goodbye :)")


def GenerateInvoice(cursor):
    cursor.execute('SELECT MAX(OrderID) FROM orders;')
    oid = cursor.fetchone()
    oid = oid[0]
                             
    orderQ = f'SELECT OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShipName, ShipAddress, ShipCity, ShipPostalCode, ShipCountry FROM orders WHERE OrderID={oid};'
    order_detailsQ = f'SELECT * FROM order_details WHERE OrderID={oid};'
                            
    cursor.execute(orderQ)
    order = cursor.fetchall()

    address = f'{order[0][6]} {order[0][7]} {order[0][8]} {order[0][9]}'
    orderDate = order[0][3].strftime("%Y-%m-%d")
    expectedDate = order[0][4].strftime("%Y-%m-%d")
    temp = [order[0][0], order[0][1], orderDate, expectedDate, order[0][5], address]
    eid = int(order[0][2])
    orderDf = pd.DataFrame([temp], columns=['Order #', 'CID', 'Order Date', 'Expected Arrival', 'Company', 'Shipping Address'])

    cursor.execute(order_detailsQ)
    order_details = cursor.fetchall()

    x = []
    totalCost = 0.00
    for i in range(len(order_details)):
        pid = order_details[i][2]
        productQ = f'SELECT ProductName, QuantityPerUnit FROM products WHERE ProductID={pid};'
        cursor.execute(productQ)
        productData = cursor.fetchall()
        temp = [productData[0][0], order_details[i][4], productData[0][1], order_details[i][3], order_details[i][5]]
        x.append(temp)
        totalCost += float(order_details[i][3] * order_details[i][4])

    order_detailsDf = pd.DataFrame(x, columns=['Product Name', 'Quantity', 'Quantity/Unit', 'Price', 'Discount'])
                            
    employeeQ = f'SELECT LastName, FirstName FROM employees WHERE EmployeeID={eid}'
    cursor.execute(employeeQ)
    employeeDf = pd.DataFrame(cursor.fetchall(), columns=['Last Name', 'First Name'])

    shippingCost = round((totalCost * .1), 2)
    totalCost = round((totalCost), 2)
    totalAndShipCost = round((shippingCost + totalCost), 2)

    print(f'\nINVOICE')
    print("-" * 60)
    print("Order #: " + orderDf['Order #'].to_string(index=False))
    print(orderDf['Company'].to_string(index=False) + "\t\tCompany ID: " + orderDf['CID'].to_string(index=False))
    print("\nOrder Date: " + orderDf['Order Date'].to_string(index=False))
    print("Expected Delivery Date: " + orderDf['Expected Arrival'].to_string(index=False))
    print("\nShipping Address\n" + orderDf['Shipping Address'].to_string(index=False))
    print("\nSales Representative\n" + employeeDf.to_string(index=False, header=False))
    print("\n\t\tPRODUCT ORDERED\n")
    print(order_detailsDf.to_string(index=False, header=False))
    print(f'\nProduct:     ${totalCost:.2f}')
    print(f'Shipping:    ${shippingCost:.2f}')
    print(f'Total:       ${totalAndShipCost:.2f}')
    print("-" * 60)
    print(f'\nPress enter to send invoice...')
    input()
    print("\nInvoice sent!")
    return 


if __name__ == '__main__':
    main()