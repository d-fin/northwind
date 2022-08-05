'''
David Finley 
DBMS Assignment 4 - Northwind 
'''
import mysql.connector as dbconn

import pandas as pd 
import numpy as np 

from UI import *
from ExecuteQuery import * 

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
                        if commit(query, None) == True: print(f'\nCustomer has been added.\n')
                        else: print(f'\nFailed to add customer.\n')

                elif choice == 2: 
                    order_detail_query, order_query, product_queries = AddOrder(cursor)
                    if order_detail_query == False or order_query == False or product_queries == False:
                        print(f'\nThere was an error submitting the order.\n')
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
                            print(f'{e}\nCannot submit order.\n')
                        else: 
                            print("\nSuccessfully submitted order!\n")

                elif choice == 3:
                    orderQuery, orderDetailQuery = RemoveOrder(cursor) 
                    if orderQuery == None or orderDetailQuery == None or orderDetailQuery == False or orderQuery == False: 
                        print("\nCannot remove order\n")
                    else:
                        try: 
                            cursor.execute('START TRANSACTION')
                            cursor.execute(orderDetailQuery)
                            cursor.execute(orderQuery)
                            db.commit()
                        except Exception as e: 
                            print(e)
                            print("\nCannot remove order.\n")
                
                elif choice == 4:
                    query = ShipOrder(cursor)

                elif choice == 5:
                    query = PrintPendingOrders(cursor)
                    if query == True: pass 
                    else: print("\nThere was an error displaying the pending orders.\n")
                
                elif choice == 6: 
                    RestockParts(cursor)

                elif choice == 7:
                    choice = MoreOptions()
                    if choice == 1: 
                        query = DisplayAllProducts(cursor)

                elif choice == 8:
                    break 
        except Exception as e:
            print(e)
        finally:
            db.rollback()
            db.close()
            print("Goodbye :)")

    

if __name__ == '__main__':
    main()