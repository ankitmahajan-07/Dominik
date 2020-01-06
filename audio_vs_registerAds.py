import psycopg2

def registerAds():
    try:
        connection = psycopg2.connect(user="verifyrecordsaccess",
                                      password="SLZHyyk39lABeL3i",
                                      host="164.68.97.194",
                                      port="",
                                      database="catalog_registerads")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        query = "SELECT owner_ad from registration_ads"
        cursor.execute(query)
        records = list(cursor.fetchall())
        records = sortList(records,4)
        print("You are connected to - ", records, "\n")

    except (Exception, psycopg2.Error) as error:
        if error != 'day is out of range for month':
            print("Error while connecting to PostgreSQL", error)
        else:
            pass
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return records

def audio_92():
    try:
        connection = psycopg2.connect(user="verifyrecordsaccess",
                                      password="SLZHyyk39lABeL3i",
                                      host="164.68.97.194",
                                      port="",
                                      database="recognition_audiofinger9sec")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        query = "SELECT detected_ad from audio9_ad_92"
        cursor.execute(query)
        records = list(cursor.fetchall())
        records = sortList(records, 7)
        print("You are connected to - ", records, "\n")

    except (Exception, psycopg2.Error) as error:
        if error != 'day is out of range for month':
            print("Error while connecting to PostgreSQL", error)
        else:
            pass
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return records

def audio_102():
    try:
        connection = psycopg2.connect(user="verifyrecordsaccess",
                                      password="SLZHyyk39lABeL3i",
                                      host="164.68.97.194",
                                      port="",
                                      database="recognition_audiofinger9sec")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        query = "SELECT detected_ad from audio9_ad_102"
        cursor.execute(query)
        records = list(cursor.fetchall())
        records = sortList(records, 7)
        print("You are connected to - ", records, "\n")

    except (Exception, psycopg2.Error) as error:
        if error != 'day is out of range for month':
            print("Error while connecting to PostgreSQL", error)
        else:
            pass
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return records

def sortList(getList, cut):
    sortedList = []
    for item in getList:
        if item[0][0:-cut].lower() not in sortedList:
            sortedList.append(item[0][0:-cut].lower())
    return sortedList


regiserAdsList = registerAds()
print(len(regiserAdsList))
audio92List = audio_92()
print(len(audio92List))
audio_102List = audio_102()
print(len(audio_102List))

print("Comparing audio9_Ad_92 with register ads")
f = open('output.txt', 'a', encoding="utf-8")
f.write('Comparing audio9_Ad_92 with register ads : '+'\n')
for item in audio92List:
    if item not in regiserAdsList:
        print(item)
        f.write(item+ ' is present in audio9_ad_92 but not in register ads'+'\n')

print('Comparing audio9_Ad_92 with register ads')
f.write('Comparing audio9_Ad_102 with register ads : '+'\n')
for item in audio_102List:
    if item not in regiserAdsList:
        f.write(item+ ' is present in audio9_ad_102 but not in register ads'+'\n')

f.close()