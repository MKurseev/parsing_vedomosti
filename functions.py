import time
import datetime
import numpy as np
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


def list_of_url_titles(date, markers_wild):
    urls, titles = [], []

    date = date.strftime('%Y/%m/%d')
    url = 'https://www.vedomosti.ru/archive/' + date

    ##########
    driver = webdriver.Chrome()  # here you should download driver show folder path
    ##########

    try:

        driver.get(url=url)  # open the link

        ### search articles on page
        xpath = "//a[@class = 'article-preview-item articles-preview-list__item']"
        articles = driver.find_elements(by=By.XPATH, value=xpath)

        count_articles_in_page = len(articles)  # count atricles from page

        if count_articles_in_page != 0:  # if there is at least one article on page

            for article in articles:

                article_title = article.text  # title
                article_url = article.get_attribute('href')  # url

                bag_of_words_title = clear_title(article_title)  # clear title from ,.:;'\"-?!/<>

                ### check if there is at least one match with article title and
                count_word_in_article_title = markers_wild[0].apply(lambda w: word_in_srting(w, bag_of_words_title)).sum()

                if count_word_in_article_title != 0:  # there is a match
                    urls.append(article_url)
                    titles.append(article_title)

    except Exception:
        print('there is a mistake this date' + str(date))
        print('____')

    finally:
        driver.close()
        driver.quit()

    return urls, titles


def copy_text_from_article(url):

    ##########
    driver = webdriver.Chrome()  # here you should download driver show folder path
    ##########

    try:
        # open the link
        driver.get(url=url)

        # find text from article
        paragraps = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class = 'article-boxes-list article__boxes']")))

        article_text = paragraps.text

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

    return article_text


def make_first_letter_capital(word):
    return ' ' + word[1:].capitalize() if word[0] == ' ' else word.capitalize()


def word_in_srting(word, string):
    return word in string


def create_wild_markers(markers):
    markers_wild = markers.copy()

    for word in markers:
        cap_word = make_first_letter_capital(word)
        markers_wild.append(cap_word)

    markers_wild = pd.DataFrame(markers_wild)
    return markers_wild


def clear_title(title):
    exclude = set(",.:;'\"-?!/<>")
    return "".join([(ch if ch not in exclude else " ") for ch in title]) + ' '


##################
markers = [' пол ', 'половой ', 'половому ', 'половые ', 'половым ', 'половыми ', 'гендер ', 'семья ', 'семью ',
           'семье ', 'семьей ', 'семьями ', 'семьи ', 'семьянин ', 'семейный', 'семейные ', 'семейному ',
           'семейным ', 'семейными ', 'мужской ', 'мужскому ', 'мужским ', 'мужские ', 'мужскими ', 'женский ',
           'женскому ', 'женским ', 'женскими ', 'феминный ', 'феминному ', 'феминным ', 'феминные ', 'феминизм',
           'феминизму', 'феминизмом', 'феминность', 'феминностью', 'феминности', 'маскулинным', 'маскулинностью',
           'маскулинному', 'маскулинизация', 'маскулинизацией', 'маскулинизации', 'маскулинный ', 'маскулинность',
           'мать ', 'матерью ', 'матери ', 'матерями ', 'матерям ', 'отец ', 'отца ', 'отцу ', 'отцом ', 'отцами ',
           'отцам ', 'сын ', 'дочь ', 'дочери ', 'дочерям ', 'дочерью ', 'дочерями ', 'дочерьми ', ' гей ', ' геи ',
           ' гею ', ' геям ', ' геем ', ' геями ', 'лгбт ', 'лесбиянка ', 'лесбиянке ', 'лесбиянки ', 'лесбиянкой ',
           'лесбиянками ', 'лесбиянкам ', 'трансперсона ', 'трансперсоне ', 'трансперсоной ', 'трансперсоны ',
           'трансперсонами ', 'трансперсонам ', 'трансгендер ', 'трансгендеру ', 'трансгендером', 'трансгендеры',
           'трансгендерам', 'трансгендерами', 'педераст', 'педик ', 'суррогатное материнство',
           'суррогатного материнства', 'суррогатному материнству', 'суррогатным материнством', 'домашнее насилие',
           'домашнему насилию', 'домашнем насилием', 'домашнем насилии', 'насильник ', 'патриархат ',
           'патриархальные ', 'патриархальный ', 'патриархальному ', 'патриархальным ', 'патриархальных ',
           'патриархальная ', 'патриархальную ', 'патриархальной ', 'материнство ', 'материнству ', 'материнством ',
           'материнствами ', 'материнства ', 'материнствам ', 'отцовство ', 'отцовству ', 'отцовствами',
           'отцовствам ', 'отцовства ', 'гомо ', 'гомосексуал', 'гомосексуалу', 'гомосексуалом', 'гомосексуалами',
           'гомосексуалы', 'гомосексуалам', 'гомосексуала', 'гомосексуальность', 'гомосексуальности',
           'гомосексуальностью', 'гомосексуальностям', 'гомосексуальностями', 'гомосексуалист', 'гомосексуалисту',
           'гомосексуалистом', 'гомосексуалисты', 'гомосексуалистам', 'гомосексуалиста', 'гомосексуалистов',
           'мужество', 'мужеству', 'мужеством', 'мужества', 'мужественность', 'мужественности', 'мужественностью',
           'женственность', 'женственный', 'женственностью', 'женственности', 'женственному', 'женственным',
           'женственными', 'женственная', 'женственной', 'женственную', 'женоподобный', 'женоподобному',
           'женоподобным', 'женоподобные', 'женоподобными', 'женственные', 'мужественные',
           'мужественными', 'мужественная', 'мужественной', 'мужественным', 'матриархат', 'матриархату',
           'матриархатом', 'матриархатный', 'матриархатному', 'матриархатными', 'матриархатным', 'женщин', 'мужчин']