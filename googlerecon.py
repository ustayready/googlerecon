#!/usr/bin/python3
'''
MIT License

Copyright (c) 2016 Michael Felch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import argparse,sys,requests,re
from bs4 import *

class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser=Parser()
parser.add_argument('domain')
args=parser.parse_args()

def google_scrape(domain):
    CHECKS = {
        "Directory Listing":"intitle:index.of site:{}",
        "Configuration Files":"ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext    :txt | ext:ora | ext:ini site:{}",
        "Database Files":"ext:sql | ext:dbf | ext:mdb site:{}",
        "Database Dumps":"ext:sql 'phpMyAdmin SQL Dump' site:{}",
        "Log Files":"ext:log site:{}",
        "Backup Files":"ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup site:{}",
        "Login Pages":"inurl:login site:{}",
        "SQL Error Pages":"intext:'sql syntax near' | intext:'syntax error has occured' | intext:'incorrect syntax near' | intext:'unexpected end of SQL command' | intext:'Warning: mysql_connect()'' | intext:'Warning: mysql_query()' | intext:'Warning: pg_connect()' site:{}",
        "Exposed Docs":"ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:cvs site:{}",
        "phpinfo()":"ext:php intitle:phpinfo 'published by the PHP Group' site:{}",
        "Private Keys":"ext:key intext:'BEGIN RSA PRIVATE KEY' site:{}",
        "Source Code Repos":"inurl:.git/ | inurl:.svn/ site:{}"
    }

    try:
        for check in CHECKS.items():
            print('[!] Checking ' + check[0])

            query = check[1].format(domain)
            url = 'https://www.google.com/search?q={}'.format(query)
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            links = soup.find_all("h3", class_="r")

            for link in links:
                a = link.findAll('a')[0].attrs['href']
                p = re.compile(r'^\/url\?q=(.*)\&sa')
                raw_link = re.findall(p, a)[0]
                print(raw_link)

            print("")
    except:
        print("Search failed")

def main(args):
    results = google_scrape(args.domain)

if __name__ == '__main__':
    main(args)

