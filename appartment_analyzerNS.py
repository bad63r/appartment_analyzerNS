import requests
from bs4 import BeautifulSoup
import sys

import aans.functions as aans


################################################################################
# def scanApparNum_nsGroup_website(url):                                       #
#     print("Starting scaning the website NS_group_nekretnine...")             #
#                                                                              #
#     # open with GET method                                                   #
#     resp = requests.get(url)                                                 #
#                                                                              #
#     # http_respone 200 means OK status                                       #
#     if resp.status_code == 200:                                              #
#         print("--> Successfully opened the web page")                        #
#                                                                              #
#         # we need a parser,Python built-in HTML parser is enough .           #
#         soup = BeautifulSoup(resp.text, 'html.parser')                       #
#                                                                              #
#         # raw_result is data which contains all the text of                  #
#         # all <p> from ns- group -nekretnine website                         #
#         print("--> Reading the number of all aparments...")                  #
#         raw_result = soup.find("p", {"class": "total_results"})              #
#                                                                              #
#         # extract important data from all <p>                                #
#         result_chunk_list = []                                               #
#         for i in raw_result.findAll("span"):                                 #
#             result_chunk_list.append(i.text)                                 #
#                                                                              #
#         # extract just the number of apartments on all Limans in             #
#         # Novi Sad on current date                                           #
#         num_of_appar_data = result_chunk_list[1]                             #
#                                                                              #
#         # adding every appartment to database                                #
#         print("--> Adding every appartment to database")                     #
#         raw_result = soup.findAll("a", {"class": "property_item_more"})      #
#         result_chunk_list = []                                               #
#         print(raw_result)                                                    #
#         for i in raw_result:                                                 #
#             result_chunk_list.append(str(i).split("\"")[3])                  #
#                                                                              #
#         appar_cnt = 1                                                        #
#         for n in result_chunk_list:                                          #
#             print("----> Reading appartment {} info".format(appar_cnt))      #
#                                                                              #
#             # open with GET method                                           #
#             url = "https://www.nekretnine-novisad.rs/" + n[2:]               #
#             resp = requests.get(url)                                         #
#                                                                              #
#             # http_respone 200 means OK status                               #
#             if resp.status_code == 200:                                      #
#                                                                              #
#                 # we need a parser,Python built-in HTML parser is enough .   #
#                 soup = BeautifulSoup(resp.text, 'html.parser')               #
#                                                                              #
#                 print("--> Successfully opened the appartment info")         #
#                 raw_result = soup.find("div", {"class": "property_details"}) #
#                 for i in raw_result:                                         #
#                     print(i.text)                                            #
#                 sys.exit(1)                                                  #
#                                                                              #
#             else:                                                            #
#                 print("Error")                                               #
#                 return 0                                                     #
#                                                                              #
#             appar_cnt = appar_cnt + 1                                        #
#                                                                              #
#         return num_of_appar_data                                             #
#     else:                                                                    #
#         print("Error")                                                       #
#         return 0                                                             #
################################################################################


def oglasi_rs_scan_website(url):
    print("Starting scaning the website oglasi.rs ...")

    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("--> Successfully opened the web page")

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')

        # raw_result is data which contains all the text of all <p> from
        # ns-group-nekretnine website
        raw_result = soup.find("div", {"class": "panel panel-default"})

        # extract important data from all <p>
        result_chunk_list = []
        for i in raw_result.findAll("span"):
            result_chunk_list.append(i.text)

        result_chunk_list = result_chunk_list[0].split("\n")
        result_chunk_list = result_chunk_list[1].replace(" ", "")

        # extract just the number of apartments on all
        # Limans in Novi Sad on current date
        num_of_appar_data, tail = result_chunk_list.split("oglasa")

        return num_of_appar_data
    else:
        print("Error")
        return 0









# extract date as dd_mm_yyyy string
date = aans.get_date()

# ns-group nekretnine url
ns_group_nekretnine_url = "https://www.nekretnine-novisad.rs/nekretnine/stan.php\
?str=1&sort=datum&filter=city:67|area:170,171,169,168|type:stan&l="

# access_url
ns_group_soup = aans.access_url(ns_group_nekretnine_url)

# scan ns-group-nekretnine website for appartmant number on Limans(1,2,3,4)
appartmant_number = aans.scanApparNum_nsGroup_website(ns_group_soup)

# connect to DabaBase. If does not exist, create one.
aans.connect_to_db()

# store data into database
aans.db_store_data("NS_group_nekretnine", "Limans", appartmant_number, date)

# create graph with results from database
aans.make_graph()





###############################################################################################################################
# # oglasi.rs                                                                                                                 #
# oglasi_rs_url = "https://www.oglasi.rs/oglasi/nekretnine/prodaja/stanova/grad/novi-sad/deo/liman-1+liman-2+liman-3+liman-4" #
# appartmant_number = oglasi_rs_scan_website(oglasi_rs_url)                                                                   #
# connect_to_db()                                                                                                             #
# db_store_data("oglasi.rs", "Limans", appartmant_number, date)                                                               #
###############################################################################################################################


