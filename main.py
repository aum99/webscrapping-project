import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

try:
    os.remove('movie.csv')
finally:
    pass

CITY = input("Type the name of your city from the list below: ").lower()
print("-----------------------------------------------")
service = Service(r"/Users/aumravibattul/Developer/chromedriver")
DRIVER = webdriver.Chrome(service=service)

try:
    if CITY == 'delhi':
        CITY = 'national-capital-region-ncr'
    DRIVER.get(f'https://in.bookmyshow.com/explore/home/{CITY}')

    def get_movie(num):
        try:
            movie = DRIVER.find_element(By.XPATH,
                                        f'//*[@id="super-container"]/div[2]/div[3]/div[1]/div[1]/div/div/div/div'
                                        f'[2]/div/div[1]/div[{num}]/a/div/div[2]/div/img')
        except NoSuchElementException:
            movie = DRIVER.find_element(By.XPATH,
                                        f'//*[@id="super-container"]/div[2]/div[3]/div[1]/div[1]/div/div/div/div'
                                        f'[2]/div/div[1]/div[{num}]/a/div/div[2]/div/div/img')

        movie.click()
        time.sleep(2)
        movie_header = DRIVER.find_element(By.XPATH, '//*[@id="super-container"]/div[2]/section[1]/div/div/div[2]/h1')
        name = movie_header.get_attribute("innerText")
        print(f'Movie: {name}')
        try:
            movie_rating = DRIVER.find_element(By.XPATH,
                                               '// *[ @ id = "super-container"] / div[2] / section[1] / div / div / div[2]'
                                               ' / section[1] / div / span[1]')
            rating = movie_rating.get_attribute("innerText")
            print(f'Rating: {rating}')
        except NoSuchElementException:
            print("The movie was released recently, so no audience rating is available currently... ")
            rating = '--'
        except:
            print("**The movie is not yet out**")
            upcoming_movie_rating = DRIVER.find_element(By.XPATH,
                                                        '// *[ @ id = "super-container"] / div[2] / section[1] / div / div'
                                                        ' / div[2] / section / div[2] / div[1] / div / span[1]')
            rating = upcoming_movie_rating.get_attribute("innerText")
            print(f'Rating: {rating} people interested')

        about = DRIVER.find_element(By.XPATH, '//*[@id="component-1"]/section/span/div/span')
        about_text = about.get_attribute("innerText")
        print(f'About Movie: {about_text}')
        print("-----------------------------------------------")
        info = f'\n{name}, {rating}, {about_text}'
        with open('movie.csv', 'a') as file:
            file.writelines(info)
        DRIVER.back()
        time.sleep(2)


    print(f"HERE ARE TOP TRENDING MOVIES IN {CITY.upper()}")
    print("-----------------------------------------------")
    for i in range(1, 11):
        if i > 5:
            html = DRIVER.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.DOWN)
            time.sleep(2)
            next = DRIVER.find_element(By.XPATH,
                                       '//*[@id="super-container"]/div[2]/div[3]/div[1]/div'
                                       '[1]/div/div/div/div[2]/div/div[2]')
            next.click()
            time.sleep(5)
            get_movie(i)
        else:
            get_movie(i)

except NoSuchElementException:
    print(f'Sorry your city is not listed in our service cities..\nWe hope to reach there soon one day')
    quit()




