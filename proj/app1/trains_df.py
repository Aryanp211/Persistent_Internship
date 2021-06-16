# import csv
# import selenium.webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# User defined variables for data retreival
 # Date as 1st command line argument.
def train_call(destCity,destStn,srcCity,srcStn,trDate):
    """ The following is the Base Url for fetching data from MakeMyTrip Website.
    	This URL appears in the search bar after origin, destination and date inputs on the landing page.
    	Thus, this URL can be changed based on User Inputs and required data can be fetched.
    """
    # baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary=" + origin + "-" + destin + "-" + trDate + "&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E"
    baseDataUrl = "https://railways.makemytrip.com/railways/listing/?classCode=&date=" + trDate + "&destCity=" + destCity + "&destStn=" + destStn + "&srcCity=" + srcCity + "&srcStn=" + srcStn
    try:

        driver = webdriver.Chrome(ChromeDriverManager().install())
        # Chrome driver is being used.
        print("Requesting URL: " + baseDataUrl)

        driver.get(baseDataUrl)  # URL requested in browser.
        print("Webpage found ...")

        element_xpath = '//*[@class="right-side-container"]/div[2]'  # First box with relevant flight data.
        print(element_xpath)
        # Wait until the first box with relevant flight data appears on Screen
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        # Scroll the page till bottom to get full data available in the DOM.
        print("Scrolling document upto bottom ...")
        for j in range(1, 100):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Find the document body and get its inner HTML for processing in BeautifulSoup parser.
        body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
        # print(body)
        print("Closing Chrome ...")  # No more usage needed.
        driver.quit()  # Browser Closed.

        print("Getting data from DOM ...")
        soupBody = BeautifulSoup(body, features="html.parser")  # Parse the inner HTML using BeautifulSoup
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------
        # Extract the required tags
        a_name_l = soupBody.findAll('div', class_='single-train-detail')

        print(
            '------------------------------------------------------------------------------------------------------------------------------------')
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        # print(a_name_l)
        a_name = []
        for x in a_name_l:
            for y in range(len(x.find('div', class_='trainSubsChild'))):
                a_name.append(x.find('div', class_='train-name').text)

        print(a_name)
        print(len(a_name))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        a_name_dur = []
        for x in a_name_l:
            for y in range(len(x.find('div', class_='trainSubsChild'))):
                a_name_dur.append(x.find('div', class_='depart-time').text)

        print(a_name_dur)
        print(len(a_name_dur))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        a_name_arri = []
        for x in a_name_l:
            for y in range(len(x.find('div', class_='trainSubsChild'))):
                a_name_arri.append(x.find('div', class_='arrival-time').text)

        print(a_name_arri)
        print(len(a_name_arri))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        a_name_dur1 = []
        for x in a_name_l:
            for y in range(len(x.find('div', class_='trainSubsChild'))):
                a_name_dur1.append(x.find('span', class_='duration').text)

        print(a_name_dur1)
        print(len(a_name_dur1))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        a_name_class = soupBody.findAll('div', attrs={"class": "card"})
        # a_name_clssss = soupBody.findAll('div', class_='trainSubsChild')

        print(len(a_name_class))
        a_name_arr = []
        list_cls = ['1A', '2A', '3A', 'SL', '2S']

        for x in a_name_class:
            a_name_arr.append(x.find('div', class_='rail-class').text)

        print(a_name_arr)
        print(len(a_name_arr))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        # a_name_pric = soupBody.findAll('div', class_='ticket-price justify-flex-end')
        a_name_pricee = []
        for x in a_name_class:
            TrainCost=list(x.find('div', class_='ticket-price justify-flex-end').text)[2:]
            TrainCostStr=''.join(map(str,TrainCost))
            TrainCostFinal=int(TrainCostStr)
            a_name_pricee.append(TrainCostFinal)
                

        print(a_name_pricee)
        print(len(a_name_pricee))
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        Train_Details = pd.DataFrame(
            {'Train name': a_name,
             'Departure time': a_name_dur,
             'Arrival Time': a_name_arri,
             'Duration': a_name_dur1,
             'Class': a_name_arr,
             'Cost': a_name_pricee
             })
        # print(len(pArrivalCity))
        print(Train_Details)
        return Train_Details

        # Train_List = data




    except Exception as e:
        print(str(e))

# EOF

# print(train_call("Delhi","NDLS","Nagpur","NGP","20210906"))