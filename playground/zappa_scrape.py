import grequests
from collections import defaultdict
from bs4 import BeautifulSoup as bs
import multiprocessing
import webbrowser,random
from bidurdb.db import __get_db_instance

def compose_zappa_search_url(search_word):
    return ZAPPA_SEARCH_URL + search_word


def create_urls_using_keywords(key_words):
    urls = []
    for key_word in key_words:
        urls.append(compose_zappa_search_url(key_word))
    return urls

def get(url):
    async_response = grequests.get(url).send()
    return async_response,url

def open_urls_in_webbrowser(urls_dict):
    for key,value in urls_dict.items():
        webbrowser.open_new_tab(random.choice(value))

def url_to_db_format(url):
    return url.replace('.','')

def create_zappa_results_dict(zappa_response_list):
    results_dict = defaultdict(list)
    for async_response,request_url in zappa_response_list:
        soup = bs(async_response.response.text, 'html.parser')
        all_links = soup.findAll('a')
        for link in all_links:
            href = link.get('href')
            if str(href).find('Show') != -1:
                results_dict[url_to_db_format(request_url)].append(ZAPPA_BASE_URL+href)
    return results_dict

def create_zappa_requests_pool(urls):
    requests_list = [pool.apply_async(get, args=(url,)) for url in urls]
    pool.close()
    pool.join()
    return requests_list


def main():
    global urls
    zappa_requests_list = create_zappa_requests_pool(urls)
    response_list = [req.get() for req in zappa_requests_list]
    results_dict = create_zappa_results_dict(response_list)
    print(results_dict)
    db = __get_db_instance()
    db.get_collection('zappa').insert_many([results_dict])
    #open_urls_in_webbrowser(results_dict)


if __name__ == '__main__':
    import time
    t1 = time.time()
    key_words = ['הרצליה', 'תל אביב', 'ירושלים']
    pool = multiprocessing.Pool()
    ZAPPA_BASE_URL = 'https://www.zappa-club.co.il/'
    ZAPPA_SEARCH_URL = ZAPPA_BASE_URL + 'AllShows?free='
    urls = create_urls_using_keywords(key_words)
    main()
    t2 = time.time()
    print('runtime:',t2-t1)