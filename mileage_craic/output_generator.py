import random
import requests
import bs4


def get_soup(path):
    """
    :param path: URL
    :return: "beautiful soup" object (HTML object)
    """
    result = requests.get(path)
    try:
        result.raise_for_status()
    except Exception:
        print("There was a problem: %s" % (Exception))

    # return soup, aka html object
    soup = bs4.BeautifulSoup(result.text, 'html.parser')

    return soup


def get_html(path, selectas):
    # get_html_object
    soup = get_soup(path)

    #select data with css selector
    results = []
    #print(len(selectas))
    for selecta in selectas:

        elements = soup.select(selecta)
        elementLength = len(elements)
        if elementLength == 0:
            print("selecta didn't work. Length = %s\n%s\n%s\nplease re-callibrate" % (elementLength, path, selecta))
        else:
            # convert to text
            for element in elements:
                output = element.getText()
                results.append(output)
    return results


def temp_check(temp):
    temp_int = int(temp.strip("°"))
    if temp_int <= 5:
        return "Pure baltic!"
    elif temp_int > 26:
        return ": Scorcher."
    elif temp_int > 18:
        return "Nice and warm."
    else:
        return ""


def weather_check(forecast):
    if "sun" in forecast.lower():
        return "Lovely sunny day."
    elif any(x in forecast for x in ["rain", "showers"]):
       return "Miserable day"
    else:
        return ""


def get_temperatures(URL):
    Hook = [".wr-value--temperature--c"]
    temperatures = get_html(URL, Hook)
    return temperatures


def get_forecasts(URL):
    ForecastSelectors = []
    for i in range(1,2):
        ForecastSelectors.append(f"div.wr-day-summary > div > span:nth-child({i})")
    forecasts = get_html(URL, ForecastSelectors)
    return forecasts


def construct_weather_text():
    URL = 'https://www.bbc.co.uk/weather/2645006'
    from mileage_craic.models import get_json_data
    URL = get_json_data("weather_url")
    temperatures = get_temperatures(URL)
    tonightTemp = temperatures[0]
    forecasts = get_forecasts(URL)
    output = " ".join([tonightTemp, forecasts[0], ". " + weather_check(forecasts[0]), temp_check(tonightTemp)])
    return output

