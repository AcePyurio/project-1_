def search_user(username, connection1):
    # Assume 'connection1' is the established connection to the database
    
    # Execute query to search for the user
    cursor = connection1.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    
    # Close the cursor
    #cursor.close()
    
    # Check if the user exists
    if user:
        return True
    else:
        return False