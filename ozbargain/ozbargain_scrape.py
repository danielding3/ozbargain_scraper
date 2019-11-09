from bs4 import BeautifulSoup
import requests
import csv
import sys

MAX_PAGES = 49

def expiredItem(node):
    isExpired = False
    for c in node['class']:
        if c == 'expired' or c == 'soldout':
            isExpired = True
    return isExpired

def search(node, itemTitle, csv_writer):
    itemLink = "www.ozbargain.com.au" + node.h2.a['href']
    print(itemTitle)
    print(f"{itemLink}")

    csv_writer.writerow([itemTitle, itemLink])
            
    print("\n--------------\n")

def scrapePage(csv_writer, itemsToLookFor):
#looping through every page
    for i in range(MAX_PAGES):
        source = requests.get(f"https://www.ozbargain.com.au/cat/electrical-electronics?page={i}")
        soup = BeautifulSoup(source.text, 'lxml')
        #Grabbing deal from every page
        for node in soup.find_all('div', class_='node-ozbdeal'):
            #skip expired/sold out items
            if expiredItem(node) == True:
                continue
            try:
                itemTitle = node.h2.a.text
                if any(keyword.lower() in itemTitle.lower() for keyword in itemsToLookFor):
                    search(node, itemTitle, csv_writer)
                elif len(itemsToLookFor) == 0:
                    search(node, itemTitle, csv_writer)
                pass
            except expression as identifier:
                pass

def prompt():
    itemsToLookFor = []
    print("Type in the items you would like to add to the search.")
    print("Leave blank and press CTRL+C if you want to search for all")
    print("Press the enter key after each item, and press CTRL+C once you have finished: ")
    while True:
        try:
            item = input()
            itemsToLookFor.append(item)
            pass
        except KeyboardInterrupt:
            break
    return itemsToLookFor


csv_file = open('ozbargain_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Deal', 'Link'])

itemsToLookFor = prompt()
scrapePage(csv_writer, itemsToLookFor)

csv_file.close()
print("Search Finished")
sys.exit()
