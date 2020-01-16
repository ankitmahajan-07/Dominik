import psycopg2
from datetime import date

def connectToDb(Database):

    connection = psycopg2.connect(user="verifyrecordsaccess",
                                  password="SLZHyyk39lABeL3i",
                                  host="164.68.97.194",
                                  port="",
                                  database=Database)

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    # print(connection.get_dsn_parameters(), "\n")
    return cursor,connection

def updateHomepage():
    cursor,connection = connectToDb("catalog_registerads")
    query = "SELECT id FROM company_name ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    records = cursor.fetchone()
    return records[0]

def countCountries():
    cursor,connection = connectToDb("catalog_registerads")
    query = "SELECT country FROM countries_countries"
    cursor.execute(query)
    records = cursor.fetchall()
    country = []
    for record in records:
        if record not in country:
            country.append(record)
    print(f'There are {len(country)} countries at present in countries_countries table.')
    return len(country)


def countAds():
    cursor,connection = connectToDb('catalog_registerads')
    query = "select owner_ad from registration_ads"
    cursor.execute(query)
    records = cursor.fetchall()
    return len(records)

def recognize_channels():
    cursor,connection = connectToDb('recognition_audiofinger9sec')
    query = "select table_name from information_schema.tables where table_schema = 'public'"
    cursor.execute(query)
    records = cursor.fetchall()
    num = 0
    for record in records:
        if record[0][:9] == 'audio9_ad':
            num+=1
    return num

def numOfDays(year,mon, day):
    today = getToday()
    date1 = date(int(today[0]), int(today[1]), int(today[2]))
    date2 = date(year,mon,day)
    return int((date1 - date2).days)

def getToday():
    Date = date.today()
    Date = str(Date).split('-')
    return Date


companies = updateHomepage()
countries = countCountries()
num_of_ads = countAds()
rec_channels = recognize_channels()
days = numOfDays(2019,11,30)
hours = days*24

print(companies, countries, num_of_ads,rec_channels,days,hours)
changes = [companies,countries, num_of_ads,rec_channels,hours,days]
# Updating records in Homepage content
for i in range(1,7):
    cursor,connection  = connectToDb('django_adsrecognition')
    query = 'update homepage_content set value=%s where id=%s'
    cursor.execute(query,(changes[i-1],i))
    connection.commit()
print("Updated data into hmepage content.")