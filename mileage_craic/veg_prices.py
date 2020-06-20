import requests, bs4, csv

# Get price data from internet
# Save to csv
# Shows prices to customer or farmer
# Organic food prices from https://www.soilassociation.org/farmers-growers/market-information/price-data/horticultural-produce-price-data/

def get_html_object(path):
    #open webpage

    result = requests.get(path)
    try:
        result.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))

    # return soup, aka html object
    return bs4.BeautifulSoup(result.text, 'html.parser')


def webscraper_function_list(path, hook):
    """
   Finds a css selector in a web page
   Arguments:
       url - the web page to search in
       hook - the CSS selector to find
   Returns:
       a list of elements
   """
    # get_html_object
    soup = get_html_object(path)
    elems = soup.select(hook)
    return elems

def read_csv_file():
    with open('output.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return csv_reader



def get_prices_table(our_prices):
    #for n in range(10):
        #print(our_prices[n])
    #print(our_prices)

    webpage = 'https://www.soilassociation.org/farmers-growers/market-information/price-data/horticultural-produce-price-data/'
    row_selector = 'tbody > tr'
    rows = webscraper_function_list(webpage, row_selector)

    output_rows = [["veg", "wholesale", "farmshop", "supermarket", "our price"]]
    n=0
    for row in rows:
        print(our_prices[n])

        #print(our_prices[rows.index(row)])
        text=row.getText().split("\n")

        # index of non blank items
        index = [1,3,4,5]
        wanted_text = [text[i] for i in index]
        output_row = [x.replace(u'\xa0', u' ') for x in wanted_text]
        output_row.append(our_prices[rows.index(row)])
        output_rows.append(output_row)
        n+=1


    return output_rows


def make_csv_file():

    with open('output.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        our_prices = []
        for row in csv_reader:
            our_prices.append(row["our price"])





    prices_table = get_prices_table(our_prices)

    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(prices_table)





def get_veg_list():
    vegetables = []
    with open('output.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)


        for row in csv_reader:
            if row["veg"] == " ":
                continue
            else:
                vegetables.append(row["veg"])
        #print("\n".join(vegetables))
        return vegetables


def get_wanted_veg(veg_list):
    while True:
        choice = input("what do you want? ")
        matches = []
        for veg in veg_list:
            if choice in veg.lower():
                matches.append(veg)
        if len(matches) == 1:
            WantToBuy = matches[0]
            break
        elif len(matches) > 1:
            print("\n".join(matches))
            second_choice = input("What kind would you like? ")
            for match in matches:
                if second_choice in match.lower():
                    WantToBuy = match
                    return WantToBuy
                    break
            break
        elif len(matches) == 0:
            continue
    return WantToBuy


def get_price(shop_type, row, unit_amount):
    price_text = row[shop_type]
    if len(price_text) == 1:
        print("sorry, no price this week")
        price = float()
    elif "(" in price_text:
        unit_price = price_text[price_text.find('(') + 1: price_text.find(')')]
        price = float(unit_price) * float(unit_amount)
        print(f"That's £{price} please")
    elif "*" in price_text:
        unit_price = price_text.strip("*")
        price = float(unit_price) * float(unit_amount)

        print(f"That's £{price} please")
    return price


def get_shopping_list(veg_list):
    total_price = 0
    while True:
        WantToBuy = get_wanted_veg(veg_list)
        with open('output.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if WantToBuy in row["veg"]:
                    veg_text = row["veg"]
                    units = veg_text[veg_text.find('(')+1 : veg_text.find(')')]
                    veg_name = veg_text.split(' (')[0]
                    unit_amount = input(f"how many {units}s/es of {veg_name}?")
                    total_price += get_price("farmshop", row, unit_amount)
                    prices = row["farmshop"]
            quit_request = input("do you want anything else?\nPress enter to continue, or any key to exit")
            if quit_request == "":
                continue
            else:
                print(f"Your total is £{total_price}\n  Please come again!")
                break

def get_unit_price(WantToBuy):
    while True:
        with open('output.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if WantToBuy in row["veg"]:
                    veg_text = row["veg"]
                    units = veg_text[veg_text.find('(')+1 : veg_text.find(')')]
                    veg_name = veg_text.split(' (')[0]
                    prices = [row["wholesale"], row["farmshop"], row["supermarket"], row["our price"]]
                    #print(row["our price"])
                    return prices
            return "----".split()
                    #"veg", "wholesale", "farmshop", "supermarket"
                    #total_price += get_price("farmshop", row, unit_amount)
            #quit_request = input("do you want anything else?\nPress enter to continue, or any key to exit")
            #if quit_request == "":
            #    continue
            #else:
            #    print(f"Your total is £{total_price}\n  Please come again!")
            #    break





make_csv_file()
veg_list = get_veg_list()
#get_shopping_list(veg_list)