'''
############################
## Name: Jack Robinson
## Title: APP.py => Apache Parser Program.
## Description: Parses Apache Log file
## Date Created: March 11, 2018
############################
'''

import re, collections
from tabulate import tabulate

apache_log_file = open("apache_log", "r").readlines()
ip_reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
url_reg = r"\".*(\s(.*)\s).*\""
response_code_reg = r"\s(\d{3})\s"

def get_log_file(file):
    ip_list = []
    url_list = []
    response_code_list = []
    for line in file:
        ip_list.append(re.match(ip_reg, line).group(0))
        url_list.append(re.search(url_reg, line).group(2))
        response_code_list.append(int(re.search(response_code_reg, line).group(1)))

    main_options(ip_list, url_list, response_code_list)

## Top 10 requested pages and the number of requests made for each
def top_ten_requested_pages(url_list):
    headers = ["Rank", "# of Requests Made", "Requested Page"]
    counter = collections.Counter(url_list)
    sort_it = sorted(counter.items(),key=lambda x: x[1], reverse=True)[:10]
    data = sorted([(v,k) for k,v in sort_it], reverse=True)
    print(tabulate(data, headers=headers, showindex=True))

## Percentage of successful requests (anything in the 200s and 300s range)
def percentage_successful(response_code_list):
    counter = 0
    for rcl in response_code_list:
        if rcl >= 200 and rcl < 400:
            counter += 1
    percent_success = ((counter / len(response_code_list)) * 100)
    print("Percentage of Successful Requests: {}%".format(round(percent_success)))

## Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
def percentage_unsuccessful(response_code_list):
    counter = 0
    for rcl in response_code_list:
        if rcl < 200 or rcl >= 400:
            counter += 1
    percent_unsuccess = ((counter / len(response_code_list)) * 100)
    print("Percentage of Unsuccessful Requests: {}%".format(round(percent_unsuccess)))

## Top 10 unsuccessful page requests
def top_ten_unsuccessful_pages(url_list, response_code_list):
    failed_url = []
    count_it = 0
    for rcl in response_code_list:
        if rcl < 200 or rcl >= 400:
            failed_url.append(url_list[count_it])
        count_it += 1
    headers = ["Rank", "# of Unsuccessful Requests Made", "Requested Page"]
    counter = collections.Counter(failed_url)
    sort_it = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10]
    data = sorted([(v, k) for k, v in sort_it], reverse=True)
    print(tabulate(data, headers=headers, showindex=True))

## The top 10 IPs making the most requests, displaying the IP address and number of requests made
def top_ten_ips(ip_list):
    headers = ["Rank", "# of Requests Made", "IP Address"]
    counter = collections.Counter(ip_list)
    sort_it = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10]
    data = sorted([(v, k) for k, v in sort_it], reverse=True)
    print(tabulate(data, headers=headers, showindex=True))

## Option parsing to produce only the report for one of the previous points (e.g. only the top 10 urls, only the percentage of successful requests and so on)
def main_options(ip_list, url_list, response_code_list):
    headers = ["Option Number",
               "Option Description"]

    options = [["***** Quit *****"],
               ["Top 10 Requested Pages"],
               ["Percentage of Successful Requests"],
               ["Percentage of Unsuccessful Requests"],
               ["Top 10 Unsuccessful Page Requests"],
               ["Top 10 IP Address Making the Most Requests"]]
    print(tabulate(options, headers=headers, showindex=True))
    try:
        user_input = int(input("Select the parsing option: "))

        while user_input != 0:
            if user_input == 1:
                top_ten_requested_pages(url_list)
                print(tabulate(options, headers=headers, showindex=True))
                user_input = int(input("Select the parsing option: "))
            elif user_input == 2:
                percentage_successful(response_code_list)
                print(tabulate(options, headers=headers, showindex=True))
                user_input = int(input("Select the parsing option: "))
            elif user_input == 3:
                percentage_unsuccessful(response_code_list)
                print(tabulate(options, headers=headers, showindex=True))
                user_input = int(input("Select the parsing option: "))
            elif user_input == 4:
                top_ten_unsuccessful_pages(url_list, response_code_list)
                print(tabulate(options, headers=headers, showindex=True))
                user_input = int(input("Select the parsing option: "))
            elif user_input == 5:
                top_ten_ips(ip_list)
                print(tabulate(options, headers=headers, showindex=True))
                user_input = int(input("Select the parsing option: "))
            else:
                user_input = int(input("***** Invalid Selection *****\nSelect the parsing option: "))
    except ValueError as e:
        print(e)

get_log_file(apache_log_file)
