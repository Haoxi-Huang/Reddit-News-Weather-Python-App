import webbrowser
import bs4
import requests
import requests.auth


class WebScraper:
    '''
        Superclass that serves as the backbone of all HTML-based web scrapes.
    '''

    def __init__(self, url):
        '''Initializes with the instance variables for url, a Requests object and a Beautiful Soup Object.
        '''
        self.url = url

        self.webObject = requests.get(url)
        self.webObject.encoding = 'UTF-8'

        self.soup = bs4.BeautifulSoup(self.webObject.text, 'html.parser', from_encoding='UTF-8')

    def getUrl(self):
        '''Returns the url of the site to be scraped.
        '''
        return self.url

    def open(self):
        '''Opens the url in a browser.
        '''
        webbrowser.open(self.url)


class Weather(WebScraper):
    '''
        The web scraper that gets weather information from WeatherSpark given some combination of country, province,
        and city. This inherits the WebScraper superclass.
    '''
    def __init__(self, country='', province='', city=''):
        '''Initializes the Weather object with one instance variable, area.
        '''
        WebScraper.__init__(self, 'https://weatherspark.com/forecasts/yr/' + country + '/' + province + '/' + city)
        if country == '' and province == '':
            self.area = city

        elif country == '' or province == '':
            if country == '':
                self.area = province + ', ' + city

            elif province == '':
                self.area = country + ', ' + city

        else:
             self.area = country + ', ' + province + ', ' + city

    def getTemp(self, isImp):
        '''Gets the temperature of the area from WeatherSpark in the requested units.
        '''
        if isImp:
            temp = self.soup.select('div.temperature > span')[0].getText()

        else:
            if self.soup.select('div.temperature > span')[0].getText()[1].isnumeric():
                if self.soup.select('div.temperature > span')[0].getText()[2].isnumeric():
                    temp = round((int(self.soup.select('div.temperature > span')[0].getText()[:3]) - 32) * 5 / 9, 2)
                    temp = str(temp) + '°C'

                else:
                    temp = round((int(self.soup.select('div.temperature > span')[0].getText()[:2]) - 32) * 5 / 9, 2)
                    temp = str(temp) + '°C'

            else:
                temp = round((int(self.soup.select('div.temperature > span')[0].getText()[0]) - 32) * 5 / 9, 2)
                temp = str(temp) + '°C'

        return temp

    def getCond(self):
        '''Gets the conditions of the area from WeatherSpark.
        '''

        #For unknown reasons, condition data doesn't exist for certain areas, this is to make sure the program doesn't
        #crash.
        if self.soup.select('div.conditions')[0].getText()[1:-1] == 'Undefined':
            condition = 'N/A'
        else:
            condition = self.soup.select('div.conditions')[0].getText()[1:-1]

        return condition

    def getWind(self, isImp):
        '''Gets the wind speed of the area from WeatherSpark in the requested units.
        '''

        #Sometimes wind data is stored in another area of the HTML tree for certain areas, this makes sure that
        #the program can find wind data no matter what.
        if len(self.soup.select('span.unit.windSpeed')) != 0:
            if isImp:
                windSpeed = self.soup.select('span.unit.windSpeed')[0].getText()

            else:
                if self.soup.select('ul > span.unit.windSpeed')[0].getText()[0].isnumeric():
                    windSpeed = round(int(self.soup.select('ul > span.unit.windSpeed')[0].getText()[:2]) * 1.61, 2)
                    windSpeed = str(windSpeed) + ' kph'

                else:
                    windSpeed = round(int(self.soup.select('ul > span.unit.windSpeed')[0].getText()[0]) * 1.61, 2)
                    windSpeed = str(windSpeed) + ' kph'

        else:
            if isImp:
                windSpeed = self.soup.select('ul > li > span.unit.windSpeed')[0].getText()

            else:
                if self.soup.select('ul > li > span.unit.windSpeed')[0].getText()[0].isnumeric():
                    windSpeed = round(int(self.soup.select('ul > li > span.unit.windSpeed')[0].getText()[:2]) * 1.61, 2)
                    windSpeed = str(windSpeed) + ' kph'

                else:
                    windSpeed = round(int(self.soup.select('ul > li > span.unit.windSpeed')[0].getText()[0]) * 1.61, 2)
                    windSpeed = str(windSpeed) + ' kph'

        return windSpeed

    def getPressure(self, isImp):
        '''Gets the pressure of the area from WeatherSpark in the requested units.
        '''

        #For unknown reasons, pressure data doesn't exist for certain areas, this is to make sure the program doesn't
        #crash.
        if len(self.soup.select('ul > span.unit.pressure')) == 0:
            pressure = 'N/A'

        else:
            if isImp:
                pressure = self.soup.select('ul > span.unit.pressure')[0].getText()

            else:
                pressure = round(float(self.soup.select('ul > span.unit.pressure')[0].getText()[:5]) * 3.39, 2)
                pressure = str(pressure) + ' kPa'

        return pressure

    def getArea(self):
        '''Returns the area.
        '''
        return self.area

    def getTomorrowTemp(self, isImp):
        '''Gets tomorrow's temperature of the area from WeatherSpark in the requested units.
        '''
        if isImp:
            nextTemp = self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()

        else:
            if self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()[1].isnumeric():
                if self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()[2].isnumeric():
                    nextTemp = self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()[:3]
                    nextTemp = round((int(nextTemp) - 32) * 5 / 9, 2)
                    nextTemp = str(nextTemp) + '°C'

                else:
                    nextTemp = self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()[:2]
                    nextTemp = round((int(nextTemp) - 32) * 5 / 9, 2)
                    nextTemp = str(nextTemp) + '°C'
            else:
                nextTemp = self.soup.select('span.temperature-high > span.unit.temperature')[0].getText()[0]
                nextTemp = round((int(nextTemp) - 32) * 5 / 9, 2)
                nextTemp = str(nextTemp) + '°C'

        return nextTemp


class Reddit():
    '''
        The web scraper that gets the top 25 trending threads from a given subreddit in Reddit.
    '''
    def __init__(self, subreddit=''):
        '''
            Initializes the Reddit object by first authenticating via Reddit's official API and security protocols.
            Then creates an instance variable, response, that is a Response object with json information instead of
            HTML and has a header indicating its name to Reddit.
        '''
        client_auth = requests.auth.HTTPBasicAuth('RcDyRrxcCvl1Ng', 'AJXF3WM2JbEy0i6mdyDEZiJdvkc')
        post_data = {"grant_type": "password", "username": "Huang56", "password": "RedditLove13#"}
        headers = {"User-Agent": "Personal Reddit App by Huang56"}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        response.json()

        if subreddit == '':
            headers = {"Authorization": response.json()['token_type'] + ' ' + response.json()['access_token'],
                       "User-Agent": "Personal Reddit App by Huang56"}
            self.response = requests.get("https://oauth.reddit.com/", headers=headers)

        else:
            headers = {"Authorization": response.json()['token_type'] + ' ' + response.json()['access_token'],
                       "User-Agent": "Personal Reddit App by Huang56"}
            self.response = requests.get("https://oauth.reddit.com/r/" + subreddit , headers=headers)

    def getTop25(self):
        '''This method returns the names of the top 25 threads in the subreddit, a link to the source, a link to the
           Reddit comments, and the number of upvotes it has.
        '''
        counter = 1
        redditData = []

        #Using the Reddit API, all website data is returned inside a json file. This means the process to navigate
        #websites changes drastically as json data can be used like a dictionary.
        for i in self.response.json()['data']['children']:
            if i['data']['stickied'] == True:
                continue

            else:
                if len(i['data']['title']) < 35:
                    redditData.append([str(counter) + '. ' + i['data']['title'], i['data']['url'],
                                       'https://reddit.com' + i['data']['permalink'], i['data']['score']])

                else:
                    redditData.append([str(counter) + '. ' + i['data']['title'][:35] + '...', i['data']['url'],
                                        'https://reddit.com' + i['data']['permalink'], i['data']['score']])

                counter += 1

        return redditData


class News(WebScraper):
    '''
        The web scraper that gets news headlines from CBC News given what category a user wants.
        This inherits the WebScraper superclass.
    '''
    def __init__(self, category = ''):
        '''Initializes the News object with an instance variable for which category a user picked.
        '''
        if category == '':
            WebScraper.__init__(self, 'http://www.cbc.ca/news')
            self.category = 'home'

        else:
            WebScraper.__init__(self, 'http://www.cbc.ca/news/' + category)
            self.category = category

    def getTopHeadlines(self):
        '''This method returns the top headlines in the category the user picked along with the urls of the headlines.
        '''
        headlinesList = []

        for element in self.soup.select('ul.topstories-primarylist > li'):
            if len(element.select('h2 > a')[0].getText()) < 35:
                headlinesList.append([element.select('h2 > a')[0].getText(),
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

            else:
                headlinesList.append([element.select('h2 > a')[0].getText()[:35] + '...',
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

        return headlinesList

    def getSecHeadlines(self):
        '''This method returns the secondary headlines in the category the user picked along
           with the urls of the headlines.
        '''
        headlinesList = []

        #CBC News has different HTML trees for the secondary headlines depending on which category a user picked.
        #A & E is organized diffently than Tech & Sci and Health and the two of them are different than the rest.

        if self.category == 'arts':
            for element in self.soup.select('ul.promocollection-list > li'):
                if len(element.select('p')[1].getText()) < 35:
                    headlinesList.append([element.select('p')[1].getText(),
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

                else:
                    headlinesList.append([element.select('p')[1].getText()[:35] + '...',
                                          'www.cbc.ca' + element.find('a', href = True)['href']])

        elif self.category == 'technology' or self.category == 'health':
            for element in self.soup.select('ul.promocollection-list > li'):
                if len(element.select('span')[0].getText()) < 35:
                    headlinesList.append([element.select('span')[0].getText(),
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

                else:
                    headlinesList.append([element.select('span')[0].getText()[:35] + '...',
                                          'www.cbc.ca' + element.find('a', href = True)['href']])

        else:
            for element in self.soup.select('ul.moreheadlines-list > li'):
                if len(element.select('a')[0].getText()) < 35:
                    headlinesList.append([element.select('a')[0].getText(),
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

                else:
                    headlinesList.append([element.select('a')[0].getText()[:35] + '...',
                                      'www.cbc.ca' + element.find('a', href = True)['href']])

        return headlinesList

