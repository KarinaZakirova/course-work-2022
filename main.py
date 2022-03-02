import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from os.file import isfile
from os import listdir
import spacy

nlp = spacy.load("ru_core_news_sm")
query = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&transl=1&likes_min=&likes_max=&rewards_min=&date_create_min=2022-01-05&date_create_max=2022-02-05&date_update_min=2022-01-05&date_update_max=2022-02-05&title=&sort=1&rnd=152877722&find=Найти%21&p={}"


def find_links(seed):
    driver = uc.Chrome()
    with driver:
        # open the page with more links
        driver.get(seed)
    with driver:
        # find link tags
        elements = driver.find_elements_by_class_name("visit-link")
        # extract links from tags
        links = [i.get_attribute('href') for i in elements]
    driver.close()
    driver.quit()
    return links


def get_file_path(link):
    return "fanfics/" + link.split("/")[-1] + ".txt"


def get_text(link):
    driver = uc.Chrome()
    if isfile(get_file_path(link)):
    	return
    with driver:
        # open the page with text
        driver.get(link)
    try:
        with driver:
            element = driver.find_element(by="id", value="content")
            text = element.get_attribute('innerText')
        driver.close()
        driver.quit()
        return text
    except NoSuchElementException:
        # page contains no text
        print(link, "no text found")
        return ""


def named_entity_recognition(a):
    doc = nlp(a)
    named_entities = []
    for ent in doc.ents:
        named_entities.append(ent.text)        
    return named_entities


def scrape_for_fanfics(pagecount=2):
    # collect links to fanfics
    links = [get_links(query.format(page)) for page in range(1, pagecount)]
    for link in links:
    	text = get_text(link)
    	if text:
            with open(get_file_path(link), "w", encoding="utf8") as file:
                file.write(text)


def frequency(iterable):
    occurences = {}
    for i in iterable:
        if i not in occurences:
            occurences[i] = 0
        occurences[i] += 1
    return sorted(occurences.items(), key=lambda x: x[1], reverse=True)


def show_ner():
    named_entities = []
    for filename in listdir("fanfics"):
        with open("fanfics/" + filename, encoding='utf8') as file:
            named_entities.extend(named_entity_recognition(file.read()))
    for key, value in frequency(named_entities):
        print(f"{key}\t{value}")

if name == "__main__":
	scrape_for_fanfics()
	show_ner()
