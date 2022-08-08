import pandas as pd 

def DisplayAllProducts(cursor):
    try: 
        cursor.execute("SELECT DISTINCT ProductID, ProductName, SupplierID, QuantityPerUnit, UnitPrice FROM products;")
        df = pd.DataFrame(cursor.fetchall(), columns=['PID', 'Product Name', 'SID', 'Quant/Unit', 'Price'])
        cursor.execute("SELECT DISTINCT SupplierID, CompanyName FROM suppliers;")
        df2 = pd.DataFrame(cursor.fetchall(), columns=['SID', 'Supplier Name'])

    except Exception as e: print(e)

    else: 
        result = df.merge(df2, on='SID')
        result.drop(columns='SID', axis=1, inplace=True)
        print(result.to_string(index=False))

def DisplayProductsByCategories(cursor):
    while True: 
        try: 
            print("\n1. Display categories.\n2. Return to main menu.")
            choice = input()
            if choice.isdigit == False: raise Exception("\nNot an integer.")
            if int(choice) < 1 or int(choice) > 2: raise Exception("\nEnter a valid option.")
            if int(choice) == 1:
                cursor.execute('SELECT CategoryID, CategoryName FROM categories;')
                df = pd.DataFrame(cursor.fetchall(), columns=['CID', 'Category'])
                print(df.to_string(index=False))
                cursor.execute('SELECT MAX(CategoryID) FROM categories;')
                maxCID = cursor.fetchone()

                while True: 
                    try: 
                        print(f'\nEnter the CID for the category you wish to display.')
                        cid = input()
                        if cid.isdigit() == False: 
                            raise Exception("Enter a valid integer.")
                        elif int(cid) > int(maxCID[0]) or int(cid) < 1: 
                            raise Exception("CID does not exist.")
                        else: 
                            break 

                    except Exception as e: print(f'\n{e}')
            elif int(choice) == 2:
                return 

        except Exception as e: print(e)

        else:
            query = f'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock FROM products WHERE CategoryID={cid};'
            cursor.execute(query)
            productDf = pd.DataFrame(cursor.fetchall(), columns=['PID', 'Name', 'Quant/Unit', 'Price', 'Current Stock'])
            print(f'\n{productDf.to_string(index=False)}')


def DisplayCustByCompName(cursor):
    try:
        query = f'SELECT DISTINCT CustomerID, CompanyName FROM customers;'
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=['CID', 'Company Name'])
        print(f'\n{df.to_string(index=False)}')
        while True: 
            companyName = input("\nEnter company name to display all data: ")
            companyName = companyName.title()
            query = f'SELECT * FROM customers WHERE CompanyName=\'{companyName}\';'
            cursor.execute(query)
            row = cursor.fetchone()
            if row == None: print(f'\n{companyName} is not a current company.')
            else: 
                address = str(row[4]) + " " + str(row[5]) + " " + str(row[7]) + " " + str(row[8])
                data = [[row[0], row[1], row[2], row[3], address, row[9], row[10]]]
                df = pd.DataFrame(data, columns=['CID', 'Company Name', 'Contact Name', 'Contact Title', 'Address', 'Phone #', 'Fax #'])
                print(f'\n{df.to_string(index=False)}')
                print("\nPress Enter to return to main menu...")
                input()
                break 

    except Exception as e: print(e)

def DisplayEmployeeInfo(cursor):
    def menu():
        print(f'\n1. Display all info on specific employee\n2. Display heirarchy.\n3. Display hire dates.\n4. Return to main menu')
        choice = int(input())
        return choice 

    try:
        query = f'SELECT EmployeeID, LastName, FirstName, Title FROM employees;'
        cursor.execute(query)

        df = pd.DataFrame(cursor.fetchall(), columns=['EID', 'Last Name', 'First Name', 'Title'])
        print(f'\n{df.to_string(index=False)}')

        while True:
            choice = menu()
            if choice == 1: 
                print("\nEnter an employees ID number to retrieve more data. (or 0 to quit)")
                eid = int(input())

                query = f'SELECT EmployeeID, LastName, FirstName, Title, HireDate, Address, City, PostalCode, Country, HomePhone, Extension, Notes FROM employees WHERE EmployeeID=\'{eid}\';'
                cursor.execute(query)

                data = cursor.fetchone()
                address = str(data[5]) + " " + str(data[6]) + " " + str(data[7]) + " " + str(data[8]) 
                notes = str(data[11])
                data = [[data[0], data[1], data[2], data[3], data[4], address, data[9], data[10]]]
                
                df = pd.DataFrame(data, columns=['EID', 'Last Name', 'First Name', 'Title', 'Hire Date', 'Address', 'Phone #', 'Ext.'])
                print("-" * 100)
                print(f'{df.to_string(index=False)}\n\nNOTES\n{notes}')
                print("-" * 100)
            elif choice == 2:
                query = f'SELECT EmployeeID, LastName, FirstName, Title FROM employees WHERE ReportsTo IS NULL;'
                cursor.execute(query)
                bossDf = pd.DataFrame([cursor.fetchone()], columns=['EID', 'Last Name', 'First Name', 'Title'])
                print(f'\n{bossDf.to_string(index=False)}')

                query = f'SELECT EmployeeID, LastName, FirstName, Title FROM employees WHERE ReportsTo=2;'
                cursor.execute(query)
                midDf = pd.DataFrame(cursor.fetchall(), columns=['EID', 'Last Name', 'First Name', 'Title'])

                cursor.execute('SELECT LastName, FirstName FROM employees WHERE EmployeeID=2')
                midBossName = cursor.fetchone()
                midBossName = str(midBossName[1]) + " " + str(midBossName[0])
                print(f'\nThe below employees report to - {midBossName}\n\n{midDf.to_string(index=False)}')

                query = f'SELECT EmployeeID, LastName, FirstName, Title FROM employees WHERE ReportsTo=5;'
                cursor.execute(query)
                lowDf = pd.DataFrame(cursor.fetchall(), columns=['EID', 'Last Name', 'First Name', 'Title'])

                cursor.execute('SELECT LastName, FirstName FROM employees WHERE EmployeeID=5;')
                lowBossName = cursor.fetchone()
                lowBossName = str(lowBossName[1]) + " " + str(lowBossName[0])
                print(f'\nThe below employees report to - {lowBossName}\n\n{lowDf.to_string(index=False)}')

            elif choice == 3: 
                cursor.execute('SELECT LastName, FirstName, Title, HireDate FROM employees ORDER BY HireDate;')
                df = pd.DataFrame(cursor.fetchall(), columns=['Last Name', 'First Name', 'Title', 'Hire Date'])
                print(df)
                
            elif choice == 4: 
                return 
           
    except Exception as e: 
        print(e)

def ContactSupplier(cursor):
    try:
        cursor.execute('SELECT SupplierID, CompanyName FROM suppliers ORDER BY SupplierID')
        df = pd.DataFrame(cursor.fetchall(), columns=['SID', 'Supplier'])
        cursor.execute('SELECT SupplierID FROM suppliers')
        ids = [x[0] for x in cursor.fetchall()]

        print("\n" + df.to_string(index=False))
        print("\nEnter supplier ID to display contact information.")

        while True: 
            try: 
                id = input()
                if id.isdigit() == False: raise Exception("\nEnter a valid supplier ID.")
                if int(id) not in ids: raise Exception("\nID does not exist.")
                
            except Exception as e: print(e)
            else: 
                id = int(id)
                break 

        query = f'SELECT CompanyName, ContactName, ContactTitle, Address, City, PostalCode, Country, Phone, Fax, HomePage FROM suppliers WHERE SupplierID={id}'
        cursor.execute(query)
        temp = cursor.fetchall()
        supplierData = []
        for i in temp[0]:
            supplierData.append(i)
        
        address = f'{supplierData[3]} {supplierData[4]} {supplierData[5]} {supplierData[6]}'
        address = address.replace('\r', '').replace('\n', '')
        name = supplierData[0]
        if supplierData[len(supplierData) - 1] == "": homePage = None 
        else: homePage = supplierData[len(supplierData) - 1]
        phone = supplierData[7]
        if supplierData[8] == "": fax = None
        else: fax = supplierData[8]
        toDf = [supplierData[1], supplierData[2]]
        df = pd.DataFrame([toDf], columns=['Contact Name', 'Title'])
        
        dashes = 0 
        if len(address) >= len(name): dashes = (len(address) + 10)
        else: dashes = (len(name) + 10)

        print(f'\nCONTACT INFORMATION')
        print("-" * dashes)
        print(f'{name}\n{df.to_string(header=False, index=False)}')
        print(f'Phone # - {phone}\nFax # - {fax}\nAddress - {address}\n\nWebsite - {homePage}')
        print("-" * dashes)

        print("\nPress Enter to return to main menu...")
        input()

    except Exception as e: print(e)