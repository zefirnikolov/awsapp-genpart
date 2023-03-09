from essential_generators import DocumentGenerator
import os
import mysql.connector
import random
import time

counter = 0

while True:
    generate_text = DocumentGenerator()
    result_sentence = generate_text.sentence()
    result = f"{result_sentence}"

    print(f"New sentences generated: {result}")

    try:
        mydb = mysql.connector.connect(
            host = os.getenv('DB_HOST', "mariadb"),
            user = os.getenv('DB_USER', "root"),
            password = os.getenv('DB_PASS', "p12345"),
            database = os.getenv('DB_NAME', "random_facts")
        )
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO facts (fact) VALUES ('" + result + "')")
        cursor.close()
        mydb.commit()

        counter += 1

        if counter % 15 == 0:
          cursor = mydb.cursor()
          cursor.execute("TRUNCATE TABLE facts")
          cursor.close()
          mydb.commit()
          print("Cleared database table.")


    except:
        print("ERROR: Database communication error.")

    t = random.randrange(20, 40)
    print(f'Sleep for {t} seconds')
    time.sleep(t)
