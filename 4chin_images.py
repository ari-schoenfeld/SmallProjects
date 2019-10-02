from bs4 import BeautifulSoup
import os
import re
import requests
import urllib
import sys

'''
TO DO:
Create directory if it does not exist

'''
def download_image(url, directory):
    parse_url = urllib.parse.urlparse(url)
    image_name = parse_url.path.rsplit('/',1)[1]
    request = requests.get(url, allow_redirects = True)
    open(os.path.join(directory, image_name), 'wb').write(request.content)

def get_image_urls(thread_url):
    thread = requests.get(thread_url)
    soup = BeautifulSoup(thread.content, 'html.parser')
    urls = []
    for img in soup.find_all("a", href=re.compile('is2.4chan.org')):
        urls.append(f"https:{img['href']}")
    return urls

def get_bar(index, end):
    if index == 0:
        return '|----------|'
    num_complete = int(index/end*10)
    num_incomplete = 10 - num_complete
    bar = '|'
    for i in range(num_complete):
        bar += '@'
    for i in range(num_incomplete):
        bar += '-'
    return (bar+'|')

def main():
    if len(sys.argv)-1 != 2:
        raise Exception('You must provide 2 arguments in addition to the script,\nthe thread url and the directory you want the images saved.')

    urls = get_image_urls(sys.argv[1])
    num_urls = len(urls)
    successes = 0
    failures = 0
    for index, url in enumerate(urls):
        print('\rDownloading image {:2} of {:2d} {}'.format(index+1, num_urls, get_bar(index, num_urls)), end='', flush = True)
        try:
            download_image(url, sys.argv[2])
            successes += 1
        except Exception as e:
            print(f'\nError on image url {url}')
            print(f'Exception: [{e}]')
            failures += 1
    print('\rDonwloading image {:2d} of {:2d} {}'.format(num_urls, num_urls, get_bar(num_urls, num_urls)), flush = True)
    print('Finished downloading images.\nSuccesses: {:2d} | Failures: {:2d}'.format(successes, failures))


if __name__ == "__main__":
    main()