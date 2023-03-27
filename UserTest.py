import psycopg2
import pandas as pd
import time

# Set up a connection to the PostgreSQL database
while True:
    start_time = time.time()
    try:
        conn = psycopg2.connect(
            dbname="agent_test",
            user="postgres",
            password="",
            host="localhost",
            port="5432",
            connect_timeout=5
        )
        print(f"Connection to PostgreSQL database successful! (Time taken: {time.time() - start_time:.2f} seconds)\nWelcome to the test apps!\n")
        break
    
    except KeyboardInterrupt:
        print(f"Connection attempt cancelled. (Time taken: {time.time() - start_time:.2f} seconds)")
    
    except Exception as e:
        print(f"Unable to connect to PostgreSQL database. Check your connection details. Error: {e}")
        continue

    # except psycopg2.OperationalError as e:
    #         if "timeout expired" in str(e):
    #             print("Timeout expired while trying to connect to PostgreSQL database. Retrying...")
    #             time.sleep(1) # Wait 1 second before retrying
    #         else:
    #             print(f"Unable to connect to PostgreSQL database. Check your connection details. (Time taken: {time.time() - start_time:.2f} seconds)")
    #             # Exit the script if there was an error connecting to the database
    #             exit()

# Open a cursor to perform database operations
cur = conn.cursor()

# Take user input for whether to insert or update a user
choice = None
while choice not in ["i", "u", "d", "sd", "su"]:
    try:
        choice = input("What would you like to do?\nEnter\n'I' for insert user\n'U' for update user\n'D' for delete user\n'SD' for show deleted user\n'SU' for show all user\nyour choose: ").lower()
    except KeyboardInterrupt:
        # Exit the script if the user presses Ctrl+C
        print("\nScript aborted.")
        exit()

if choice == 'i':
    # Take user input for name, email, and password
    username = input("Enter username: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")

    # Insert the user input into the "user" table
    try:
        cur.execute(
            "insert into user_test (id, created_at, updated_at, deleted_at, username, email, phone) VALUES (default, now(), now(), null, %s, %s, %s)",
            (username, email, phone)
        )
        # Commit the changes to the database
        conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        # Rollback the changes if there was an error and show the error message
        conn.rollback()
        print(f"An error occurred: {e}")
        print("Rolling back changes...")
        
    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")


elif choice == "u":
    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")


    # Take user input for updating a user's information
    user_id = input("\nEnter ID of user to update: ")
    new_username = input("Enter username: ")
    new_email = input("Enter email: ")
    new_phone = input("Enter phone: ")

    # Update the user's information in the "user" table
    try:
        if new_username:
            cur.execute(
                "UPDATE user_test SET username = %s, updated_at = now() WHERE id = %s",
                (new_username, user_id)
            )
        if new_email:
            cur.execute(
                "UPDATE user_test SET email = %s, updated_at = now() WHERE id = %s",
                (new_email, user_id)
            )
        if new_phone:
            cur.execute(
                "UPDATE user_test SET phone = %s, updated_at = now() WHERE id = %s",
                (new_phone, user_id)
            )
        # Commit the changes to the database
        conn.commit()
        print("Data updated successfully!")
    except Exception as e:
        # Rollback the changes if there was an error and show the error message
        conn.rollback()
        print(f"An error occurred: {e}")
        print("Rolling back changes...")

    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")


elif choice == "d":
    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")

    delete_multiple_or_not = input("\nDo you want delete multiple user? Enter 'y' for yes or 'n' for no: ")

    # if else for delete multiple
    if delete_multiple_or_not == 'n':
        # Take user input for updating a user's information
        user_id = input("\nEnter ID of user to delete: ")

        # Update the user's information in the "user" table
        try:
            cur.execute(
                "UPDATE user_test SET deleted_at = now(), updated_at = now() WHERE id = %s",
                [user_id]
            )
            # Commit the changes to the database
            conn.commit()
            print("Data deleted successfully!")
        except Exception as e:
            # Rollback the changes if there was an error and show the error message
            conn.rollback()
            print(f"An error occurred: {e}")
            print("Rolling back changes...")

    elif delete_multiple_or_not == 'y':
        
        # user_ids = input("Enter ID(s) separated by commas: ").strip().split(',')
        # user_ids = [id.strip() for id in user_ids]
        # if all(id.isdigit() for id in user_ids):
        #     query = f"UPDATE user_test SET deleted_at = now(), updated_at = now() WHERE id IN ({','.join(['%s']*len(user_ids))})"
        #     data = tuple(user_ids)
        # else:
        #     print("Invalid ID(s). Please enter number(s) separated by commas.")
        # try:
        #     cur.execute(query,data)
        #     conn.commit()
        #     print(f"{cur.rowcount} rows updated successfully")
        # except psycopg2.Error as e:
        #     conn.rollback()
        #     print(f"An error occurred: {e}")
        #     print("Rolling back changes...")

        while True:
            user_ids = input("Enter ID(s) separated by commas: ").strip().split(',')
            user_ids = [id.strip() for id in user_ids]
            if all(id.isdigit() for id in user_ids):
                break
            else:
                print("Invalid ID(s). Please enter number(s) separated by commas.")

        for id in user_ids:
            try:
                cur.execute("UPDATE user_test SET deleted_at = now(), updated_at = now() where id in (%s)", [int(id)])
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error deleting data for ID {id}: {e}")

        # print(f"Data for ID(s) {', '.join(user_ids)} inserted successfully.")

    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")

elif choice == "sd":
    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is not null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
        
        # restore user
        restore_user = input("\nDo you want to restore the user? Enter 'y' for yes or 'n' for no: ").lower()
        if restore_user == 'y':
            
            # restore all user or not
            restore_user_all_or_not = input("\nOk! Do you want to restore all user? Enter 'y' for yes or 'n' for no: ").lower()

            if restore_user_all_or_not == 'n':
                # Take user input for updating a user's information
                user_id = input("\nEnter ID of user to restore: ")

                # Update the user's information in the "user" table
                try:
                    cur.execute(
                        "UPDATE user_test SET deleted_at = null, updated_at = now() WHERE id in (%s)",
                        [user_id]
                    )
                    # Commit the changes to the database
                    conn.commit()
                    print("User data restored successfully!")
                except Exception as e:
                    # Rollback the changes if there was an error and show the error message
                    conn.rollback()
                    print(f"An error occurred: {e}")
                    print("Rolling back changes...")

            elif restore_user_all_or_not == 'y':
                # Update the user's information in the "user" table
                try:
                    cur.execute(
                        "UPDATE user_test SET deleted_at = null, updated_at = now() WHERE deleted_at is not null"
                    )
                    # Commit the changes to the database
                    conn.commit()
                    print("All data user restored successfully!")
                except Exception as e:
                    # Rollback the changes if there was an error and show the error message
                    conn.rollback()
                    print(f"An error occurred: {e}")
                    print("Rolling back changes...")

        elif restore_user == 'n':
            print("Ok!")
            cur.close()
            conn.close()

        else:
            print("Wrong Choose!")
            cur.close()
            conn.close()

    else:
        print("There is no user has been deleted.")

elif choice == 'su':
    # Show the entire "user" table
    cur.execute("SELECT id, username, email, phone FROM user_test where deleted_at is null order by id")
    rows = cur.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'NAME', 'EMAIL', 'PHONE NUMBER'])
        # format columns for better readability
        print("\nAll data in table:\n")
        print(df.to_string(index=False))
    else:
        print("There is no user has been deleted.")

# Close the cursor and connection to the database
cur.close()
conn.close()