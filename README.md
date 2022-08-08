# Northwind

# Installation Instructions 
- Machine used is a mac running the latest version of MacOS.
- These install instructions assume python and mysql is installed. 

# Install Python dependencies 
- Navigate to the requirements.txt file in northwind project folder.
    ```
    pip3 install -r requirements.txt
    ```

# Create Database
- Start mysql in Mac settings
    ```
    $ mysql -u root -p
    mysql> CREATE database northwind;
    ```

- Navigate to sql file location 
    ```
    $ mysql -u root -p northwind < northwind_assign4.sql
    ```

# Create User 
    ```
    mysql> CREATE USER 'cs4430'@'localhost' IDENTIFIED WITH mysql_native_password BY 'cs4430';
    mysql> GRANT ALL ON northwind.* TO 'cs4430'@'localhost';
    mysql> FLUSH PRIVILEGES;
    ```

# Run Instructions 
- Navigate to project folder location in terminal and go to folder with 'main.py'.
    ```
    $ python3 main.py 
    ```