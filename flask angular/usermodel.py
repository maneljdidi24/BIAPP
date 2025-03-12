import json


    
    
def selectUsers(cnxn):
    try: 
        sqlQuery = f"select * from users"
        cursor = cnxn.cursor()

        # Fetch all rows as a list of dictionaries
        rows = cursor.execute(sqlQuery).fetchall()
        columns = [column[0] for column in cursor.description]

        # Convert each row to a dictionary
        users_list = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        return users_list
    finally:
        cnxn.close()



    
def create_user(cnxn, Email, family_name , email, password , role):
    try:    
        cursor = cnxn.cursor()
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        sqlQuery = "INSERT INTO users (Email,password, email, password,role) VALUES (?,?,?,?,?)"
        cursor.execute(sqlQuery, (Email, password, family_name, email , password,role))
        cnxn.commit()
        return {"msg": "User created successfully.", "code": 201}
    finally:
        cnxn.close()

def getUserFromEmailPassword(cnxn, email):
    cursor = cnxn.cursor()
    sqlQuery = "SELECT * FROM users WHERE email = ?"
    cursor.execute(sqlQuery, (email))
    result = cursor.fetchone()
    if result is not None:
        # Convert the result to a dictionary for easier access
        user = {
            'id': result[0],
            'name': result[1],
            'family_name': result[2],
            'email': result[3],
            'password': result[4],
            'role': result[5]
        }
        return user
    else:
        return None  