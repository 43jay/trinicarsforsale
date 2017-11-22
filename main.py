import requests
import os.path

from lxml import html

import listing

CAR_DOMAIN = 'http://www.trinicarsforsale.com'
FEATURED_CARS_LIST = CAR_DOMAIN + '/database/featuredcarsList.php'

def run_and_get_listings():
    """Load the root page, and from there fetch all the listings."""
    print("Fetching root: %s" % FEATURED_CARS_LIST)
    page = requests.get(FEATURED_CARS_LIST)
    tree = html.fromstring(page.content)

    NUM_PAGES = tree.xpath('/html/body/table[6]/tr/td[1]/font[7]/b/text()')[0]
    NUM_PAGES = int(NUM_PAGES)
    print("Crawling {0} pages".format(NUM_PAGES))

    listings = []
    for i in range(NUM_PAGES-1):
        listings = listings + fetch_listings(tree)

        next_link = tree.xpath('/html/body/table[6]/tr/td[2]/font[4]/b/a/@href')[0]
        next_link = CAR_DOMAIN + next_link

        print('Next page: %s\n' % next_link)
        page = requests.get(next_link)
        tree = html.fromstring(page.content)

    return listings



def fetch_listings(tree):
    """We know there are 15 rows (X), 2 listings per row (Y)"""
    table_node_path = '/html/body/table[5]/tr[{0}]/td[{1}]/table/tr[1]/td[2]/font/table'

    post_id_subpath = '/tr[2]/td/font/b/a/text()'
    make_subpath = '/tr[3]/td[2]/font/text()'
    model_subpath = '/tr[4]/td[2]/font/text()'
    series_subpath = '/tr[5]/td[2]/text()'
    price_subpath = '/tr[6]/td[2]/font/b/text()'

    listings = []
    for x in range(15):
        for y in [1, 2]:
            # Pull out cars on page
            curr_path = table_node_path.format(x + 1, y)

            post_id = tree.xpath(curr_path + post_id_subpath)
            make = tree.xpath(curr_path + make_subpath)
            model = tree.xpath(curr_path + model_subpath)
            series = tree.xpath(curr_path + series_subpath)
            price = tree.xpath(curr_path + price_subpath)

            listings.append(
                listing.Listing.create(post_id, make, model, series, price))

    return listings

if __name__ == '__main__':
    with open('featuredcarsDetails.txt', 'w+') as outfile:
        LISTINGS = run_and_get_listings()
        for listing in LISTINGS:
            print(listing)
            outfile.write("{0}\n".format(str(listing)))
