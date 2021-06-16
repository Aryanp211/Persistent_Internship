import csv
import selenium.webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
# User defined variables for data retreival

def flight_call(origin,destin,trDate):
    """ The following is the Base Url for fetching data from MakeMyTrip Website.
    	This URL appears in the search bar after origin, destination and date inputs on the landing page.
    	Thus, this URL can be changed based on User Inputs and required data can be fetched.
    """
    baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary=" + origin + "-" + destin + "-" + trDate + "&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E"

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # Chrome driver is being used.
        print("Requesting URL: " + baseDataUrl)

        driver.get(baseDataUrl)  # URL requested in browser.
        print("Webpage found ...")

        element_xpath = '//*[@id="left-side--wrapper"]/div[2]'  # First box with relevant flight data.

        # Wait until the first box with relevant flight data appears on Screen
        options = webdriver.ChromeOptions()
        options.headless = True
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

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

        # Extract the required tags
        a_name_l = soupBody.findAll('div', class_='fli-list')
        print(
            '------------------------------------------------------------------------------------------------------------------------------------')
        print(
            '-----------------------------------------------------------------------------------------------------------------------------------')
        # print(a_name_l)
        a_name = []
        for x in a_name_l:
            a_name.append(x.find('span', class_='boldFont blackText airlineName').text)

        print(a_name)
        # for x in a_name:
        #     spanFlightName = x.find('p').text
        # spanFlightName = soupBody.findAll("span", class_='boldFont blackText airlineName')  # Tags with Flight Name

        # pFlightCode = soupBody.findAll("p", {"class": "fli-code"})  # Tags with Flight Code
        a_name_ts = soupBody.findAll('div', attrs={"class": "flightTimeSection"})
        a_name_dtime = []
        for x in a_name_ts:
            a_name_dtime.append(x.find('p').text)
        print(a_name_dtime)
        # divDeptTime = soupBody.findAll("div", attrs={"class": "dept-time"})  # Tags with Departure Time
        # pDeptCity = soupBody.findAll("p", attrs={"class": "dept-city"})  # Tags with Departure City
        table_cty = soupBody.findAll('div', attrs={"class": "flightTimeSection"})
        pDeptCity = []
        for x in table_cty:
            pDeptCity.append(x.find('p', class_='darkText').text)
        print(pDeptCity)
        # pFlightDuration = soupBody.findAll("p", attrs={"class": "fli-duration"})  # Tags with Flight Duration
        table_dur = soupBody.findAll('div', attrs={"class": "appendRight40"})
        pFlightDuration = []
        for x in table_dur:
            pFlightDuration.append(x.find('p').text)
        print(pFlightDuration)
        # pArrivalTime = soupBody.findAll("p", attrs={"class": "reaching-time append_bottom3"})  # Tags with Arrival Time
        # table = soupBody.findAll('div', attrs={"class": "flightTimeSection"})
        # pArrivalTime = []
        # for x in table:
        #     pArrivalTime.append(x.find('p').text)
        # #pArrivalCity = soupBody.findAll("p", attrs={"class": "arrival-city"})  # Tags with Arrival City
        # table = soupBody.findAll('div', attrs={"class": "flightTimeSection"})
        # for x in table:
        #     pArrivalCity = x.find('p').text
        # #spanFlightCost = soupBody.findAll("span", attrs={"class": "actual-price"})  # Tags with Flight Cost
        spanFlightCost_l = soupBody.findAll('div', class_='priceSection')

        spanFlightCost = []
        for x in spanFlightCost_l:
            FlightCost=list(x.find('p').text[2:])
            FlightCost.remove(',')
            FlightCostStr=''.join(map(str,FlightCost))
            FlightCostFinal=int(FlightCostStr)
            spanFlightCost.append(FlightCostFinal)  
            print('55555555555555555555555')
            print(x.find('p').text[2:])
            
        # FlightCost=list(spanFlightCost)
        # FlightCost.remove(',')
        # FlightCostStr=''.join(str,FlightCost)
        # FlightCostFinal=int(FlightCostStr)
        # print('22222222222222222222222222222222222')
        # print(FlightCostFinal)


        # Data Headers
        flightsData = [["flight_name", "departure_time", "departure_city", "flight_duration", "arrival_time",
                        "arrival_city", "flight_cost"]]
        list_dept_time = a_name_dtime[::2]
        list_arr_time = a_name_dtime[1::2]
        list_dept_city = a_name_dtime[::2]
        list_arr_city = a_name_dtime[1::2]
        # print(len(spanFlightName))
        # print(len(pFlightCode))
        print(len(a_name))
        print(len(a_name_dtime))  # 1
        print(len(list_dept_time))
        print(list_dept_time)
        print(len(list_arr_time))
        print(list_arr_time)

        print(len(pDeptCity))  # 1
        print(len(list_dept_city))
        print(list_dept_city)
        print(len(list_arr_city))
        print(list_arr_city)
        print(len(pFlightDuration))
        # print(len(pArrivalTime))
        print(len(spanFlightCost))

        Flight_Details = pd.DataFrame(
            {'Flight Name': a_name,
             'Departure Time': list_dept_time,
             'Arrival Time': list_arr_time,
             'From': list_dept_city,
             'To': list_arr_city,
             'Duration': pFlightDuration,
             'Cost': spanFlightCost
             })
        # print(len(pArrivalCity))
        return Flight_Details

        # # Extracting data from tags and appending to main database flightsData
        # for j in range(0, len(a_name) ):
        #     flightsData.append([a_name[j].text, a_name_dtime[j].text, pDeptCity[j].text,
        #                         pFlightDuration[j].text, a_name_dtime[j].text, pDeptCity[j].text,
        #                         spanFlightCost[j].text])
        #
        # # Output File for FlightsData. This file will have the data in comma separated form.
        # outputFile = "FlightsData_" + origin + "-" + destin + "-" + trDate.split("/")[0] + "-" + trDate.split("/")[
        #     1] + "-" + trDate.split("/")[2] + ".csv"
        #
        # # Publishing Data to File
        # print("Writing flight data to file: " + outputFile + " ...")
        # with open(outputFile, 'w', newline='') as spfile:
        #     csv_writer = csv.writer(spfile)
        #     csv_writer.writerows(flightsData)
        #     print("Data Extracted and Saved to File. ")
        # # print("Records\nFlight Name: "+ str(len(a_name)) + "\nDept Time: "+ str(len(a_name_dtime)) + "\nDept City: "+ str(len(pDeptCity)) + "\nFlight Duration: "+ str(len(pFlightDuration)) + "\nArrival Time: "+ str(len(pArrivalTime)) + "\nArrival City: "+ str(len(pArrivalCity)) + "\nFlight Cost: "+ str(len(spanFlightCost)))
        # # print(flightsData)
        # # print(outputFile)
        # # print(a_name)
    except Exception as e:
        print(str(e))


# EOF

# print(flight_call("NAG","DEL","06/09/2021"))