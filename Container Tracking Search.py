from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

def searates(driver, line):
    #Initialize Chrome driver
    
    driver.get("https://www.searates.com/container/tracking/")

    #wait for 5 seconds
    sleep(5)

    #switch to iframe
    driver.switch_to.frame(0)

    #enter container number
    container = driver.find_element_by_name("container")
    container.send_keys(line)
    container.send_keys(Keys.RETURN)

    #set parameters for site not loading
    caught = False
    seconds = 0

    #Script waits until website loads or 20 seconds have passed
    while(not caught and seconds < 20):
        try:
            driver.find_element_by_class_name("container-item").click()
            last_box = driver.find_elements_by_class_name("events-list")[-1]
        except:
            print("Website not loading. Waiting {0} more seconds.".format(20-seconds))
            sleep(1)
            seconds += 1
            continue
        caught = True
        print("Website loaded. Continuing...")

    #Returns N/A if 20 seconds have passed without page loading
    if(not caught):
        return "N/A"
    box_lines = str(last_box.text).split("\n") #Searches for location and status in last updated section
    info = {}
    info["location"] = box_lines[0]
    info["target_info"] = box_lines[-1]

    return info

#Open and write to CSV
def csv_writeline(line):
    with open("Container Output.csv", "a") as file:
        file.write(line + "\n")

#Overwrites previous CSV and iterates over container numbers in input file
driver = webdriver.Chrome('./chromedriver')
with open("Container Output.csv", "w") as file:
    file.write("")
with open("Container Input.txt", "r") as readfile:
    for line in readfile:
        line = line.rstrip()
        info = searates(driver, line)
        if info == "N/A":
            #alternate_method_1(driver, line)
            csv_writeline("{0},No useful information can be output.".format(line))
        else:
            csv_writeline("{0},{1} - {2}".format(line, info["location"], info["target_info"], ))
