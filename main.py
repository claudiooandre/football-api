import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Function to connect the database
def connecter():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root1234',
                database='futebol'
            )
        return connection
    except Error as e:
        print(f"Error to connection to MySQL: {e}")
        return None

# Function to register with the username and the password
def register(connection):
    username = input("\nInsert the username: ")
    password = getpass("Insert the password: ")
    permissions = input("\nAdmin or read?")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO futebol.users (username, password, permissions) VALUES (%s, %s, %s)", (username, password, permissions))
    print("\nRegister!")

    connection.commit()
    cursor.close()

#login with the username and the password
def login(connection):
    username = input("\nInsert the username: ")
    password = getpass("Insert the password: ")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM futebol.users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        print("\nLogin successful!")
    else:
        print("\nUsername or password were incorrect.")

    cursor.close()

# Connection to the database MySQL
connection = connecter()

if connection:

    while True:

        #Main Menu
        print("\n1. Register new user")
        print("2. Login")
        print("3. Exit\n")

        opcao = input("Choose a option: ")

        #if to put 1 to check the register
        if opcao == '1':
            register(connection)
        #if to put 2 to check the login and then access to the menu
        elif opcao == '2':
            login(connection)
        
            while True:
                
                question = input('\nWhat is the club? ')

                cursor = connection.cursor()
                cursor.execute("select * from futebol.atletas where atletas.clube='"+question+"'")
                myresult = cursor.fetchall()

                if myresult:

                    question1 = input('\nWhat is the level? ')
                    
                    if question1=='senior':

                        question2 = input('\nDo you want to see/add or remove athletes?? ')
                        
                        if question2=='see':
                            cursor = connection.cursor()
                            cursor.execute("select atletas.nome from futebol.atletas where atletas.clube='"+question+"'")
                            myresult = cursor.fetchall()
                            print(myresult)

                            while True:

                                question8 = input('\nDo you want to continue? ')
                                
                                if question8=='yes':
                                    break
                                
                                elif question8=='no':
                                    print('Thank you!')
                                    exit()
                                
                                else:
                                    print("Write yes or no!")
                        
                        elif question2=='add':
                            question3 = input('\nWhat is the athlete\'s name? ')
                            question4 = input('How old is the athlete?')
                            question5 = input('What is the athlete\'s weight? ')
                            question6 = input('How tall is the athlete? ')  
                            cursor = connection.cursor()
                            cursor.execute("insert into futebol.atletas(nome,idade,peso,altura,clube) values ('"+question3+"',"+question4+","+question5+",'"+question6+"','"+question+"')")
                            myresult = cursor.fetchall()
                            connection.commit()
                            
                            while True:

                                question7 = input('\nQueres adicionar mais algum atleta? ')
                            
                                if question7=='yes':
                                    question3 = input('\nWhat is the athlete\'s name? ')
                                    question4 = input('How old is the athlete?')
                                    question5 = input('What is the athlete\'s weight? ')
                                    question6 = input('How tall is the athlete? ')        
                                    cursor = connection.cursor()
                                    cursor.execute("insert into futebol.atletas(nome,idade,peso,altura,clube) values ('"+question3+"',"+question4+","+question5+",'"+question6+"','"+question+"')")
                                    myresult = cursor.fetchall()
                                    connection.commit()
                                    continue

                                elif question7=='no':
                                    print('Thank you!')
                                    exit()
                                else:
                                    print("Write yes or no!")
                            
                        elif question2=='remove':

                            question9 = input('\nWhich athlete\'s name would you like to delete? ')

                            cursor = connection.cursor()
                            cursor.execute("delete from futebol.atletas where atletas.nome='"+question9+"'")
                            myresult = cursor.fetchall()
                            connection.commit()
                            
                            while True:
                        
                                question10 = input('\nDo you want to delete any more athletes? ')
                            
                                if question10=='yes':
                                    question11 = input('\nWhich athlete\'s name would you like to delete? ')
                                    cursor = connection.cursor()
                                    cursor.execute("delete from futebol.atletas where atletas.nome='"+question11+"'")
                                    myresult = cursor.fetchall()
                                    connection.commit()
                                    continue

                                elif question10=='no':
                                    print('Thank you!')
                                    exit()
                                
                                else:
                                    print("Write yes or no!")
                    
                    else:
                        print("Write the level correctly!")
                    
                else:
                    print("Write the club name correctly!")

        elif opcao == '3':
            print("Goodbye my friend!")
            exit()
