import os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service(log_path=os.path.devnull)
driver = webdriver.Firefox(options=firefox_options, service=service)

#def getLongestTitle(tabs): #get the longest tab name to format list
#    max = 0
#    for tab in tabs:
#        if len(tab[1]) > max:
#            max = len(tab[1])
#    return max

def getTab(url,title,artist):
    os.system('cls')
    driver.get(url)

    tabInfo = driver.find_elements(By.CLASS_NAME, value='_1qDg._3aoCP')
    print(' '*2 + title,'by',artist)
    for line in tabInfo:
        print(' '*2 + line.text)
    print()

    #line class = _3rlxz
    lines = driver.find_elements(By.CLASS_NAME, value='_3rlxz')
    for line in lines:
        print(' '*2 + line.text)
    
    if input('\n  Press Enter to go back (0 to quit): ') == '0':
        driver.quit()
        sys.exit()

def indexTabs(url):
    tabList = []
    driver.get(url)
    tabNames =  driver.find_elements(By.CLASS_NAME, value='_2pBsi')
    tabArtist = driver.find_elements(By.CLASS_NAME, value='_1Nq0G')
    tabType = driver.find_elements(By.CLASS_NAME, value='_2amQf._2Fdo4')
    tabScore = driver.find_elements(By.CLASS_NAME, value='_2amQf._3LNtq')
    tabLinks = driver.find_elements(By.CLASS_NAME, value='JoRLr._3dYeW')

    for i in range(len(tabNames)):
        if tabType[i].text != 'Official' and 'Pro' not in tabType[i].text: #filter out pro & official tabs
            tabList.append([tabArtist[i].text , tabNames[i].text , tabScore[i].text , tabLinks[i].get_attribute('href') , tabType[i].text])
        else:
            if tabArtist[i].text != '':
                tabList.append(['NA',tabArtist[i].text]) #return artist of official song so it appears in list
    return tabList

def searchTabs(search):

    pageNum = 1
    #Types
    #0 - all
    #200 - tabs
    #300 - chords

    type = '0'
    if ' tab' in search:
        type = '200'
    elif 'chord' in search:
        type = '300'

    while True:
        os.system('cls')
        url = 'https://www.ultimate-guitar.com/search.php?title='+search+'&page='+str(pageNum)+'&type='+type
        tabs = indexTabs(url)
        #max = getLongestTitle(tabs)

        for index in range(len(tabs)):
            tab = tabs[index]
            if tab[0] == 'NA':
                print('\n'+tab[1])
                continue

            tabArtist = tab[0]
            tabName = tab[1]
            #if "\n" in tabName: #removing time from pro and official tabs 
            #    tabName = tabName[0:tabName.find('\n')]
            tabScore = tab[2]
            tabType = tab[4]
            if tabScore == '':
                tabScore = '0'
            if tabArtist != '':
                print(tabArtist) #print new artist when encountered
            #print(' '*10  , '['+str(index+1)+']' , tabName , 'Score:' , tabScore , tabType)
            print(' '*12 + "{:>2s} {:45} {:>8s} {:>10s} ".format('['+str(index+1)+']',tabName,tabScore,tabType))
        
        while True:
            choice = input('\nPage '+ str(pageNum)+ '| Tab Number (prev/next to change page, 0 to exit): ').lower()
            if choice == '0':
                driver.quit()
                sys.exit()
            elif 'n' in choice:
                pageNum += 1
                break
            elif 'p' in choice:
                if pageNum == 1:
                    print('Invalid Input')
                else:
                    pageNum -= 1
                    break
            elif choice.isalpha() == False:
                if int(choice) <= len(tabs):
                    choice = int(choice)-1
                    getTab(tabs[choice][3],tabs[choice][1],tabs[choice][0])
                    break
                else:
                    print('Invlaid Input')
            else:
                print('Invalid Input')


def main(search):
    searchTabs(search)
main('+'.join(sys.argv[1:]))