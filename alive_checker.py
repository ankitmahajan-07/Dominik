import psycopg2
from datetime import date
import subprocess
from os import path
import os
import shutil

audio_folder = "/var/www/html/public/userfiles/Audio"
video_folder = "/var/www/html/public/userfiles/Video"
countries = {"Slovakia" : "svk"}
folders = ["4", "6", "9"]


def numOfDays(date1, date2):
    return int((date1 - date2).days)

def getToday():
    Date = date.today()
    Date = str(Date).split('-')
    return Date


def move_record(owner_ad, country):
    print('Moving this file : ',owner_ad)
    audio_files = []
    video_files = []
    for i in folders:
        for j in range(9):
            audio_files.append("{}00{}.aac".format(owner_ad, j))
        for j in range(9):
            video_files.append("{}00{}.mp4".format(owner_ad, j))
        for j in audio_files:
            if path.exists("{0}{1}/{2}/{3}".format(audio_folder, i, countries[country], j)):
                print("{0}{1}/{2}/{3}".format(audio_folder, i, countries[country], j))
                shutil.move("{0}{1}/{2}/{3}".format(audio_folder, i, countries[country], j),
                            "{0}{1}/{2}/expired/".format(audio_folder, i, countries[country]))
        for j in video_files:
            if path.exists("{0}{1}/{2}/{3}".format(video_folder, i, countries[country], j)):
                print("{0}{1}/{2}/{3}".format(video_folder, i, countries[country], j))
                shutil.move("{0}{1}/{2}/{3}".format(video_folder, i, countries[country], j),
                            "{0}{1}/{2}/expired/".format(video_folder, i, countries[country]))


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
    query = "SELECT id,expiry_date,date_time,owner_ad,country from registration_ads"
    cursor.execute(query)
    records = list(cursor.fetchall())
    # print(records)
    for record in records:
        if record[1] == 'Never':
            print('In never')
            today = getToday()
            date1 = date(int(today[0]), int(today[1]), int(today[2]))
            date2 = str(record[2]).split('_')[0]
            date2 = date2.split('-')
            date2= date(int(date2[0]),int(date2[1]),int(date2[2]))
            diff = numOfDays(date1,date2)
            if diff/30 >= 24:
                print("Status is older than 24 months, declaring expired and moving files.")
                move_record(record[3], record[4])
                try:
                    print('Alive to 0')
                    new_query = """UPDATE registration_ads SET alive=%s and expiry_date=%s WHERE id=%s;"""
                    print(new_query, "new query")
                    cursor.execute(new_query, ('0','expired' ,record[0]))
                    connection.commit()
                except (Exception, psycopg2.Error) as error:
                    print("Could not update records on database", error)
            else:
                try:
                    print('Record is never so setting alive to 1')
                    new_query = """UPDATE registration_ads SET alive=%s WHERE id=%s;"""
                    print(new_query, "new query")
                    cursor.execute(new_query, ('1', record[0]))
                    connection.commit()
                except (Exception, psycopg2.Error) as error:
                    print("Could not update records on database", error)
        else:
            today = getToday()
            getDateFromDb = str(record[1]).split('-')
            date1 = date(int(today[0]), int(today[1]), int(today[2]))
            if getDateFromDb[2] == '00':
                getDateFromDb[2] = '01'
            date2 = date(int(getDateFromDb[0]), int(getDateFromDb[1]), int(getDateFromDb[2]))
            print(date1, date2)
            diff = numOfDays(date1, date2)
            if diff >= -1:
                try:
                    print('Alive to zero and moving files')
                    move_record(record[3], record[4])
                    new_query = """UPDATE registration_ads SET alive=%s WHERE id=%s;"""
                    print(new_query, "new query")
                    cursor.execute(new_query, ('0', record[0]))
                    connection.commit()
                except (Exception, psycopg2.Error) as error:
                    print("Could not update records on database", error)
            else:

                try:
                    print('Alive to 1')
                    new_query = """UPDATE registration_ads SET alive=%s WHERE id=%s;"""
                    print(new_query, "new query")
                    cursor.execute(new_query, ('1', record[0]))
                    connection.commit()
                except (Exception, psycopg2.Error) as error:
                    print("Could not update records on database", error)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")