import requests
from bs4 import BeautifulSoup
import datetime 
import sqlite3
import matplotlib.pyplot as plt
import sys

def ns_group_scan_website(url):
    print("Starting scaning the website NS_group_nekretnine...")

    #open with GET method
    resp=requests.get(url)
      
    #http_respone 200 means OK status
    if resp.status_code==200:
        print("--> Successfully opened the web page")
      
        # we need a parser,Python built-in HTML parser is enough .
        soup=BeautifulSoup(resp.text,'html.parser')    
  
        # raw_result is data which contains all the text of all <p> from ns-group-nekretnine website
        print("--> Reading the number of all aparments...")
        raw_result=soup.find("p",{"class":"total_results"})

        # extract important data from all <p>
        result_chunk_list = []
        for i in raw_result.findAll("span"):
            result_chunk_list.append(i.text)

        # extract just the number of apartments on all Limans in Novi Sad on current date
        num_of_appar_data = result_chunk_list[1]

        # adding every appartment to database
        print("--> Adding every appartment to database")
        raw_result=soup.findAll("a",{"class":"property_item_more"})
        result_chunk_list = []
        print(raw_result)
        for i in raw_result:
            result_chunk_list.append(str(i).split("\"")[3])

        appar_cnt = 1
        for n in result_chunk_list:
            print("----> Reading appartment {} info".format(appar_cnt))

            #open with GET method
            url = "https://www.nekretnine-novisad.rs/" + n[2:]
            resp=requests.get(url)


            #http_respone 200 means OK status
            if resp.status_code==200:

                # we need a parser,Python built-in HTML parser is enough .
                soup=BeautifulSoup(resp.text,'html.parser')    

                print("--> Successfully opened the appartment info")
                raw_result=soup.find("div",{"class":"property_details"})
                for i in raw_result:
                    print(i.text)
                sys.exit(1)

            else:
                print("Error")
                return 0
                
            appar_cnt = appar_cnt + 1
            




        return num_of_appar_data
    else:
        print("Error")
        return 0



def oglasi_rs_scan_website(url):
    print("Starting scaning the website oglasi.rs ...")

    #open with GET method
    resp=requests.get(url)
      
    #http_respone 200 means OK status
    if resp.status_code==200:
        print("--> Successfully opened the web page")
      
        # we need a parser,Python built-in HTML parser is enough .
        soup=BeautifulSoup(resp.text,'html.parser')    
  
        # raw_result is data which contains all the text of all <p> from ns-group-nekretnine website
        raw_result=soup.find("div",{"class":"panel panel-default"})

        # extract important data from all <p>
        result_chunk_list = []
        for i in raw_result.findAll("span"):
            result_chunk_list.append(i.text)

        result_chunk_list = result_chunk_list[0].split("\n")
        result_chunk_list = result_chunk_list[1].replace(" ","")

        # extract just the number of apartments on all Limans in Novi Sad on current date
        num_of_appar_data, tail = result_chunk_list.split("oglasa")



        return num_of_appar_data
    else:
        print("Error")
        return 0

def get_date():
    current_date_and_time = datetime.datetime.now()
    year = current_date_and_time.year
    month = current_date_and_time.month
    day = current_date_and_time.day

    date = str(day)+"_"+str(month)+"_"+str(year)

    return date

def connect_to_db():

    # Connecting to sqlite
    conn = sqlite3.connect('appartment_analyzerNS.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # check if table exists
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='APPARTMENTS' ''')

    if cursor.fetchone()[0] == 0:
        print('--> Creating appartment_analyzerNS database...')


        # Creating table
        table ="""CREATE TABLE APPARTMENTS(WEBSITE TEXT, CITY_LOC TEXT, NUM_OF_APPAR INTEGER, DATE TEXT);"""
        cursor.execute(table)

        # Commit your changes in the database    
        conn.commit()

        # Closing the connection
        conn.close()
    else:
        print('--> appartment_analyzerNS database exists! Database connecting...')


    
def db_store_data(website, city_loc, num_of_appar, date):

    # Connecting to sqlite
    conn = sqlite3.connect('appartment_analyzerNS.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # check if entry for current date exist. If that is true, do not enter new value into database
    entry_exist = False
    dates_list = cursor.execute("SELECT DATE FROM APPARTMENTS")
    for row in dates_list:
        if date == row[0]:
            entry_exist = True
  
    # Queries to INSERT records.
    if not entry_exist:
        cursor.execute("INSERT INTO APPARTMENTS (WEBSITE, CITY_LOC, NUM_OF_APPAR, DATE) VALUES (?, ?, ?, ?)",\
                       (website, city_loc, num_of_appar, date))

    # Commit your changes in the database    
    conn.commit()


    # Closing the connection
    conn.close()

def make_graph():
    # Connecting to sqlite
    conn = sqlite3.connect('appartment_analyzerNS.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # extract num of appartments for ns_group_nekretnine website
    ns_group_data_appar_num = cursor.execute(''' SELECT NUM_OF_APPAR FROM APPARTMENTS WHERE WEBSITE = "NS_group_nekretnine" ''')

    # parsing num_of_appr extracted data for ns_group_nekretnine
    ns_group_data_appar_num_list = []
    ns_group_data_dates_list = []
    print("TEST TEST:")
    for row in ns_group_data_appar_num:
        ns_group_data_appar_num_list.append(int(row[0]))

    # extract dates for ns_group_nekretnine website that are in connection with num of appartments of the same website
    ns_group_data_dates     = cursor.execute(''' SELECT DATE FROM APPARTMENTS WHERE WEBSITE = "NS_group_nekretnine" ''')

    # parsing dates extracted data for ns_group_nekretnine
    for row in ns_group_data_dates:
        ns_group_data_dates_list.append((row[0]))
        
    print(ns_group_data_dates_list)

    # assigning value for plot axis
    ns_group_date_axis_graph      = ns_group_data_dates_list
    ns_group_appar_num_axis_graph = ns_group_data_appar_num_list


    # plotting the points
    plt.plot(ns_group_date_axis_graph, ns_group_appar_num_axis_graph, label = "ns_group_nekretnine")
    #plt.plot(oglasi_rs_date_axis_graph, oglasi_rs_appar_num_axis_graph, label = "oglasi.rs")
    plt.legend()

    # naming the x axis
    plt.xlabel('date')
    # naming the y axis
    plt.ylabel('num of apartmants on Limans')

    # giving a title to my graph
    plt.title('Appartment_analyzerNS')

    # function to show the plot
    plt.show()

    # Closing the connection
    conn.close()

  


date = get_date()

# ns-group nekretnine
ns_group_nekretnine_url = "https://www.nekretnine-novisad.rs/nekretnine/stan.php?str=1&sort=datum&filter=city\:67|area:170,171,169,168|type:stan&l="
appartmant_number = ns_group_scan_website(ns_group_nekretnine_url)
connect_to_db()
db_store_data("NS_group_nekretnine", "Limans", appartmant_number, date)


# oglasi.rs
oglasi_rs_url = "https://www.oglasi.rs/oglasi/nekretnine/prodaja/stanova/grad/novi-sad/deo/liman-1+liman-2+liman-3+liman-4"
appartmant_number = oglasi_rs_scan_website(oglasi_rs_url)
connect_to_db()
db_store_data("oglasi.rs", "Limans", appartmant_number, date)



make_graph()
