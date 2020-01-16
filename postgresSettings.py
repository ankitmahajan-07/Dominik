import psycopg2, os
from datetime import date


def numOfDays(date1, date2):
    return int((date1 - date2).days)

def getToday():
    Date = date.today()
    Date = str(Date).split('-')
    return Date



try:
    connection = psycopg2.connect(user = "verifyrecordsaccess",
                                  password = "SLZHyyk39lABeL3i",
                                  host = "164.68.97.194",
                                  port = "",
                                  database = "catalog_registerads")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    query = "SELECT * from records_location"
    cursor.execute(query)
    records = list(cursor.fetchall())
    print("You are connected to - ", records,"\n")

    for record in records:
        record = list(record)
        print(record)
        today = getToday()
        getDateFromDb = record[1].split('-')
        date1 = date(int(today[0]),int(today[1]), int(today[2]))
        if getDateFromDb[2] == '00':
            getDateFromDb[2] = '01'
        date2 = date(int(getDateFromDb[0]), int(getDateFromDb[1]), int(getDateFromDb[2]))
        print(date1, date2)
        try:
            diff = numOfDays(date1,date2)
            print(diff, type(diff), 'difference')
        except:
            continue
        if diff == 5:
            cmd = 'rm -r reordings/'+record[1]
            try:
                print("Folder is older than required days. Will delete that.")
                os.system(cmd)
                try:
                    print("Files are not present on this user's pc. Setting alive to 0")
                    new_query = """UPDATE records_location SET alive=%s WHERE id=%s;"""
                    print(new_query, "new query")
                    cursor.execute(new_query, (0, record[0]))
                    connection.commit()
                except (Exception, psycopg2.Error) as error:
                    print("Could not update records on database", error)
            except:
                print('Cannot delete directory')
        else:
            if record[-1] != 0:
                current_ip = record[-3]
                current_path = record[-2]
                cmd = current_path
                if os.path.exists(cmd):
                    try:
                        print("Files are present on this user's pc, setting alive to 1")
                        new_query = """UPDATE records_location SET alive=%s WHERE id=%s;"""
                        print(new_query, "new query")
                        cursor.execute(new_query,(1,record[0]))
                        connection.commit()
                    except (Exception, psycopg2.Error) as error:
                        print("Could not update records on database",error)
                else:
                    try:
                        print("Files are not present on this user's pc. Setting alive to 0")
                        new_query = """UPDATE records_location SET alive=%s WHERE id=%s;"""
                        print(new_query, "new query")
                        cursor.execute(new_query, (0,record[0]))
                        connection.commit()
                    except (Exception, psycopg2.Error) as error:
                        print("Could not update records on database",error)

except (Exception, psycopg2.Error) as error :
    if error != 'day is out of range for month':
        print ("Error while connecting to PostgreSQL", error)
    else:
        pass
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")