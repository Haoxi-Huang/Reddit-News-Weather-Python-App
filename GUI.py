from graphics import *
from button import *
from WebClasses import *
import webbrowser


class MainGUI:
    '''
        Class MainGUI is the starting point for launching any application inside the Omni-App. It is the user's
        first interaction with the Omni-App. The GUI has four buttons with 3 for launching the other applications.
    '''

    def __init__(self):
        '''This constructor method initializes the Main Menu GUI which is a GraphWin object.
        '''
        self.win = GraphWin('Start', 400, 400)
        self.win.setCoords(0, 0, 400, 400)

        background = Image(Point(200, 200), 'Main Title 2.gif')
        background.draw(self.win)
        self.weatherButton = Button(self.win, Point(80, 200), 80, 20, 'Weather')
        self.redditButton = Button(self.win, Point(200, 200), 80, 20, 'Reddit')
        self.newsButton = Button(self.win, Point(320, 200), 80, 20, 'News')
        self.quitButton = Button(self.win, Point(200, 35), 80, 20, 'Quit')
        self.quitButton.activate()
        self.weatherButton.activate()
        self.redditButton.activate()
        self.newsButton.activate()

    def run(self):
        '''This method runs the Main Menu GUI and accepts and interprets user clicks.
        '''
        buttonList = [self.weatherButton, self.redditButton, self.newsButton]

        pt = self.win.getMouse()

        while not self.quitButton.clicked(pt):
            for button in buttonList:
                if button.clicked(pt):
                    if button == self.weatherButton:
                        gui = WeatherGUI()
                        gui.run()

                    elif button == self.redditButton:
                        gui = RedditGUI()
                        gui.run()

                    elif button == self.newsButton:
                        gui = NewsGUI()
                        gui.run()

            pt = self.win.getMouse()

        self.win.close()


class WeatherGUI:
    '''
        Class WeatherGUI is the user's destination for weather information. The user enters area information
        and then clicks a button to find out relevant weather information. The GUI features 6 buttons with 3 entry boxes
        for entering area information.
    '''

    def __init__(self):
        '''This initializes the Weather GUI which is a GraphWin object as well as several buttons and three entry boxes.
        '''
        self.win = GraphWin('Weather', 400, 400)
        self.win.setCoords(0, 0, 400, 400)

        background = Image(Point(200, 200), 'Weather.gif')
        background.draw(self.win)

        self.quitButton = Button(self.win, Point(200, 35), 80, 20, 'Quit')
        self.findButton = Button(self.win, Point(300, 125), 80, 20, 'Find')
        self.detailButton = Button(self.win, Point(140, 300), 80, 20, 'Details')
        self.fileButton = Button(self.win, Point(260, 300), 80, 20, 'File')
        self.impButton = Button(self.win, Point(140, 200), 80, 20, 'Imperial')
        self.metButton = Button(self.win, Point(260, 200), 80, 20, 'Metric')

        self.errorText = Text(Point(200, 240), '')
        self.unitsDisplay = Text(Point(300, 150), '')
        self.displayLine1 = Text(Point(200, 280), '')
        self.displayLine2 = Text(Point(200, 260), '')
        self.displayLine3 = Text(Point(200, 240), '')
        self.displayLine4 = Text(Point(200, 220), '')

        self.findButton.activate()
        self.quitButton.activate()
        self.impButton.activate()
        self.metButton.activate()

        self.errorText.draw(self.win)
        self.unitsDisplay.draw(self.win)
        self.displayLine1.draw(self.win)
        self.displayLine2.draw(self.win)
        self.displayLine3.draw(self.win)
        self.displayLine4.draw(self.win)

        self.city = Entry(Point(175, 100), 10)
        self.province = Entry(Point(175, 135), 10)
        self.country = Entry(Point(175, 170), 10)

        self.country.draw(self.win)
        self.province.draw(self.win)
        self.city.draw(self.win)


    def run(self):
        '''This method runs the Weather GUI and accepts user input in entry boxes and clicks.
        '''
        firstTime = True
        findError = False
        isImp = False

        self.unitsDisplay.setText('Units: Metric')
        pt = self.win.getMouse()

        while not self.quitButton.clicked(pt):
            if self.findButton.clicked(pt):
                if self.displayLine1.getText() != '':
                    self.displayLine1.setText('')
                    self.displayLine2.setText('')
                    self.displayLine3.setText('')
                    self.displayLine4.setText('')

                try:
                    if self.city.getText() == '':
                        self.errorText.setText('Please try again. Enter a valid area for city.')
                        findError = True

                    elif self.country.getText() == '' and self.province.getText() == '':
                        weather = Weather('', '', self.city.getText())

                        if findError:
                            self.errorText.setText('')
                            findError = False

                    elif self.country.getText() == '' or self.province.getText() == '':
                        if self.country.getText() == '':
                            weather = Weather('', self.province.getText(), self.city.getText())

                            if findError:
                                self.errorText.setText('')
                                findError = False

                        elif self.province.getText() == '':
                            weather = Weather(self.country.getText(), self.city.getText())

                            if findError:
                                self.errorText.setText('')
                                findError = False

                    else:
                        weather = Weather(self.country.getText(), self.province.getText(), self.city.getText())

                        if findError:
                            self.errorText.setText('')
                            findError = False

                    if not findError:
                        self.fileButton.activate()
                        self.detailButton.activate()
                        self.findButton.deactivate()

                        self.displayLine1.setText('The temperature there is ' + weather.getTemp(isImp) + '.')
                        self.displayLine2.setText('The wind is ' + weather.getWind(isImp) + '.')
                        self.displayLine3.setText('The pressure is ' + weather.getPressure(isImp) + '.')
                        self.displayLine4.setText('Tomorrow\'s temperature is ' + weather.getTomorrowTemp(isImp) + '.')

                except:
                    findError = True

                    self.fileButton.deactivate()
                    self.detailButton.deactivate()
                    self.findButton.activate()

                    self.city.setText('')
                    self.province.setText('')
                    self.country.setText('')

                    self.errorText.setText('Please try again. The area you entered cannot be found.')

            elif self.fileButton.clicked(pt):
                if firstTime:
                    outFile = open('Weather Information.txt', 'w', encoding='UTF-8')

                    outFile.write('{:30} {:10} {:20} {:20} {:20} {:}'.format('Area', 'Temp', 'Tomorrow\'s Temp', 'Wind Speed', 'Pressure', 'Conditions\n'))
                    outFile.write('{:30} {:10} {:20} {:20} {:20} {:}'.format('****', '********', '********************', '***************', '**************', '**********\n'))

                    firstTime = False

                self.city.setText('')
                self.province.setText('')
                self.country.setText('')

                self.findButton.activate()
                self.fileButton.deactivate()
                self.detailButton.deactivate()

                outFile.write('{:30} {:10} {:20} {:15} {:>15} {:>40}'.format(weather.getArea(), weather.getTemp(isImp), weather.getTomorrowTemp(isImp), weather.getWind(isImp), weather.getPressure(isImp), weather.getCond() + '\n'))

            elif self.metButton.clicked(pt):
                isImp = False
                self.unitsDisplay.setText('Units: Metric')

            elif self.impButton.clicked(pt):
                isImp = True
                self.unitsDisplay.setText('Units: Imperial')

            elif self.detailButton.clicked(pt):
                weather.open()

            pt = self.win.getMouse()

        self.win.close()


class RedditGUI:
    '''
        Class RedditGUI is the user's hub for accessing information on Reddit.com. The user will either enter a
        subreddit or choose the front page and will then be presented with relevant headlines and options from Reddit.
        The GUI features 6 buttons with an entry box for entering a subreddit.
    '''
    def __init__(self):
        '''This initializes the Reddit GUI which is a GraphWin object along with several buttons and an entry box.
        '''
        self.win = GraphWin('Reddit', 400, 400)
        self.win.setCoords(0, 0, 400, 400)

        background = Image(Point(200, 200), 'Reddit.gif')
        background.draw(self.win)

        self.quitButton = Button(self.win, Point(200, 35), 80, 20, 'Quit')
        self.findButton = Button(self.win, Point(275, 100), 120, 20, 'Find Subreddit')
        self.frontButton = Button(self.win, Point(275, 130), 120, 20, 'Front Page')
        self.doneButton = Button(self.win, Point(200, 175), 120, 20, 'Done')
        self.sourceButton = Button(self.win, Point(280, 220), 90, 20, 'Source')
        self.commentsButton = Button(self.win, Point(120, 220), 90, 20, 'Comments')
        self.nextButton = Button(self.win, Point(375, 260), 20, 100, '>')
        self.backButton = Button(self.win, Point(25, 260), 20, 100, '<')

        self.errorText = Text(Point(200, 240), '')
        self.displayLine1 = Text(Point(200, 280), '')
        self.displayLine2 = Text(Point(200, 260), '')

        self.subreddit = Entry(Point(150, 100), 10)

        self.findButton.activate()
        self.quitButton.activate()
        self.frontButton.activate()

        self.errorText.draw(self.win)
        self.displayLine1.draw(self.win)
        self.displayLine2.draw(self.win)

        self.subreddit.draw(self.win)

    def run(self):
        '''This method runs the Reddit GUI and accepts user input in entry boxes and clicks.
        '''
        findError = True
        counter = 0

        pt = self.win.getMouse()

        while not self.quitButton.clicked(pt):
            if self.frontButton.clicked(pt):
                redditObj = Reddit()
                findError = False

            elif self.findButton.clicked(pt):
                redditObj = Reddit(self.subreddit.getText())

                if self.subreddit.getText().count(' ') > 0:
                    self.errorText.setText('Please enter a subreddit name without spaces.')
                    findError = True

                elif len(redditObj.response.json()['data']['children']) == 0:
                    self.errorText.setText('Please enter a valid subreddit.')
                    findError = True

                else:
                    findError = False

            if not findError:
                redditData = redditObj.getTop25()

                self.doneButton.activate()
                self.nextButton.activate()
                self.commentsButton.activate()
                self.sourceButton.activate()

                self.frontButton.deactivate()
                self.findButton.deactivate()

                if self.nextButton.clicked(pt):
                    self.displayLine1.setText('')
                    self.displayLine2.setText('')
                    counter += 1

                elif self.backButton.clicked(pt):
                    self.displayLine1.setText('')
                    self.displayLine2.setText('')
                    counter -= 1

                #The next four elif statements prevent the user from going too far forward or backward in the
                #top 25 thread list.
                if counter == 0:
                    self.backButton.deactivate()

                if counter == 1:
                    self.backButton.activate()

                if counter == 24:
                    self.nextButton.deactivate()

                if counter == 23:
                    self.nextButton.activate()

                self.displayLine1.setText(redditData[counter][0])
                self.displayLine2.setText('Score: ' + str(redditData[counter][3]))

                if self.commentsButton.clicked(pt):
                    webbrowser.open(redditData[counter][2])

                elif self.sourceButton.clicked(pt):
                    webbrowser.open(redditData[counter][1])

                elif self.doneButton.clicked(pt):
                    counter = 0

                    self.displayLine1.setText('')
                    self.displayLine2.setText('')

                    self.findButton.activate()
                    self.frontButton.activate()

                    self.doneButton.deactivate()
                    self.backButton.deactivate()
                    self.nextButton.deactivate()
                    self.commentsButton.deactivate()
                    self.sourceButton.deactivate()

            pt = self.win.getMouse()

        self.win.close()


class NewsGUI:
    '''
        Class NewsGUI is where the user will go to access news headlines from CBC News. The user will click
        a button to be directed to a set of headlines related to that category and will then be presented with a
        variety of options and headlines. The GUI features 15 buttons.
    '''

    def __init__(self):
        '''This initializes the News GUI which is a GraphWin object along with many buttons.
        '''
        self.win = GraphWin('News', 400, 400)
        self.win.setCoords(0, 0, 400, 400)

        background = Image(Point(200, 200), 'News.gif')
        background.draw(self.win)

        self.quitButton = Button(self.win, Point(200, 35), 80, 20, 'Quit')
        self.homeButton = Button(self.win, Point(50, 135), 100, 20, 'Home')
        self.worldButton = Button(self.win, Point(150, 135), 100, 20, 'World')
        self.canadaButton = Button(self.win, Point(250, 135), 100, 20, 'Canada')
        self.politicsButton = Button(self.win, Point(350, 135), 100, 20, 'Politics')
        self.businessButton = Button(self.win, Point(50, 95), 100, 20, 'Business')
        self.healthButton = Button(self.win, Point(150, 95), 100, 20, 'Health')
        self.aeButton = Button(self.win, Point(250, 95), 100, 20, 'A & E')
        self.techsciButton = Button(self.win, Point(350, 95), 100, 20, 'Tech & Sci')
        self.headlinesButton = Button(self.win, Point(100, 180), 120, 20, 'Headlines')
        self.secheadlinesButton = Button(self.win, Point(300, 180), 120, 20, 'More Headlines')
        self.nextButton = Button(self.win, Point(375, 260), 20, 100, '>')
        self.backButton = Button(self.win, Point(25, 260), 20, 100, '<')
        self.linkButton = Button(self.win, Point(200, 250), 120, 20, 'Full Article')
        self.doneButton = Button(self.win, Point(200, 220), 120, 20, 'Done')

        self.displayLine1 = Text(Point(200, 280), '')
        self.displayLine1.setFill('white')

        self.quitButton.activate()
        self.homeButton.activate()
        self.worldButton.activate()
        self.canadaButton.activate()
        self.politicsButton.activate()
        self.businessButton.activate()
        self.healthButton.activate()
        self.aeButton.activate()
        self.techsciButton.activate()

        self.displayLine1.draw(self.win)

    def run(self):
        '''
        This method runs the Reddit GUI and accepts user input in entry boxes and clicks.
        '''
        counter = 0
        headlineButtonClicked = False
        secHeadlineButtonClicked = False
        buttonList = [self.homeButton, self.worldButton, self.canadaButton, self.politicsButton, self.businessButton,
                      self.healthButton, self.aeButton, self.techsciButton]

        pt = self.win.getMouse()

        while not self.quitButton.clicked(pt):
            for button in buttonList:
                if button.clicked(pt):
                    if button == self.homeButton:
                        newsObj = News()

                    else:
                        if button == self.aeButton or button == self.techsciButton:
                            if button == self.aeButton:
                                newsObj = News('arts')

                            else:
                                newsObj = News('technology')

                        else:
                            newsObj = News(button.getLabel().lower())

                    self.homeButton.deactivate()
                    self.worldButton.deactivate()
                    self.canadaButton.deactivate()
                    self.politicsButton.deactivate()
                    self.businessButton.deactivate()
                    self.healthButton.deactivate()
                    self.aeButton.deactivate()
                    self.techsciButton.deactivate()

                    self.headlinesButton.activate()
                    self.secheadlinesButton.activate()

            if self.headlinesButton.clicked(pt):
                newsList = newsObj.getTopHeadlines()

                headlineButtonClicked = True

                self.secheadlinesButton.deactivate()
                self.headlinesButton.deactivate()

                self.doneButton.activate()
                self.linkButton.activate()
                self.nextButton.activate()

            elif self.secheadlinesButton.clicked(pt):
                newsSecList = newsObj.getSecHeadlines()

                secHeadlineButtonClicked = True

                self.headlinesButton.deactivate()
                self.secheadlinesButton.deactivate()

                self.doneButton.activate()
                self.linkButton.activate()
                self.nextButton.activate()

            if self.nextButton.clicked(pt):
                self.displayLine1.setText('')
                counter += 1

            if self.backButton.clicked(pt):
                self.displayLine1.setText('')
                counter -= 1

            if counter == 0:
                self.backButton.deactivate()

            if counter == 1:
                self.backButton.activate()

            if headlineButtonClicked:
                self.displayLine1.setText(newsList[counter][0])

                if self.linkButton.clicked(pt):
                    webbrowser.open(newsList[counter][1])

                if counter == len(newsList) - 2:
                    self.nextButton.activate()

                elif counter == len(newsList) - 1:
                    self.nextButton.deactivate()

            if secHeadlineButtonClicked:
                self.displayLine1.setText(newsSecList[counter][0])

                if self.linkButton.clicked(pt):
                    webbrowser.open(newsSecList[counter][1])

                if counter == len(newsSecList) - 2:
                    self.nextButton.activate()

                elif counter == len(newsSecList) - 1:
                    self.nextButton.deactivate()

            if self.doneButton.clicked(pt):
                counter = 0
                secHeadlineButtonClicked = False
                headlineButtonClicked = False

                self.displayLine1.setText('')

                self.homeButton.activate()
                self.worldButton.activate()
                self.canadaButton.activate()
                self.politicsButton.activate()
                self.businessButton.activate()
                self.healthButton.activate()
                self.aeButton.activate()
                self.techsciButton.activate()

                self.doneButton.deactivate()
                self.headlinesButton.deactivate()
                self.secheadlinesButton.deactivate()
                self.linkButton.deactivate()
                self.backButton.deactivate()
                self.nextButton.deactivate()

            pt = self.win.getMouse()

        self.win.close()
