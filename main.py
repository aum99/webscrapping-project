import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service(r"/Users/aumravibattul/Developer/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get('https://in.bookmyshow.com/explore/home/pune')


def get_movie(num):
    try:
        movie = driver.find_element(By.XPATH, f'//*[@id="super-container"]/div[2]/div[3]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/div[{num}]/a/div/div[2]/div/img')
    except:
        movie = driver.find_element(By.XPATH,f'//*[@id="super-container"]/div[2]/div[3]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/div[{num}]/a/div/div[2]/div/div/img')

    movie.click()
    time.sleep(2)
    movie_header = driver.find_element(By.XPATH, '//*[@id="super-container"]/div[2]/section[1]/div/div/div[2]/h1')
    name = movie_header.get_attribute("innerText")
    print(f'Movie: {name}')
    try:
        movie_rating = driver.find_element(By.XPATH,
                                           '// *[ @ id = "super-container"] / div[2] / section[1] / div / div / div[2] / section[1] / div / span[1]')
        rating = movie_rating.get_attribute("innerText")
        print(f'Rating: {rating}')
    except:
        print("**The movie is not yet out**")
        upcoming_movie_rating = driver.find_element(By.XPATH,
                                                    '// *[ @ id = "super-container"] / div[2] / section[1] / div / div / div[2] / section / div[2] / div[1] / div / span[1]')
        rating = upcoming_movie_rating.get_attribute("innerText")
        print(f'Rating: {rating} people interested')

    about = driver.find_element(By.XPATH, '//*[@id="component-1"]/section/span/div/span')
    about_text = about.get_attribute("innerText")
    print(f'About Movie: {about_text}')
    print("-----------------------------------------------")
    info = f'\n{name}, {rating}, {about_text}'
    with open('movie.csv', 'a') as file:
        file.writelines(info)
    driver.back()
    time.sleep(2)



print("HERE ARE TOP TRENDING MOVIES IN PUNE")

for i in range(1,11):
    if i > 5:
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.DOWN)
        time.sleep(2)
        next = driver.find_element(By.XPATH,
                                   '//*[@id="super-container"]/div[2]/div[3]/div[1]/div[1]/div/div/div/div[2]/div/div[2]')
        next.click()
        time.sleep(5)
        get_movie(i)
    else:
        get_movie(i)

