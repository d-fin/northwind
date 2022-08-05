Northwind- A UI to interact with a database. 

Installation Instructions 
- Machine used is a mac running the latest version of MacOS

# Install Python 
- brew installs pip
    ```
    $ brew install python3
    ```

# Install mySQL Server 
    ```
    $ pip3 install mysql
    ```

# Install mysql dependencies 
    ```
    $ pip3 install mysql-connector-python
    $ pip3 install mysql-python
    ```

# Install Python packages needed 
    ```
    $ pip3 install numpy
    $ pip3 install pandas
    ```

# Create Database
- Start mysql in Mac settings
    ```
    $ mysql -u root -p
    mysql> CREATE database northwind;
    ```

- Navigate to sql file location 
    ```
    mysql -u root -p northwind < northwind_assign4.sql
    ```

# Create User 
    ```
    mysql> CREATE USER 'cs4430'@'localhost' IDENTIFIED WITH mysql_native_password BY 'cs4430';
    mysql> GRANT ALL ON northwind.* TO 'cs4430'@'localhost';
    mysql> FLUSH PRIVILEGES;
    ```

Run Instructions 
