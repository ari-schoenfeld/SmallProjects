import os
import sys
import re
import requests
import datetime
import urllib
from bs4 import BeautifulSoup

exclusions = ['/bbg/']
inclusions = []

def get_image_urls(thread_url):
    thread = requests.get(thread_url)
    soup = BeautifulSoup(thread.content, 'html.parser')
    urls = []
    for img in soup.find_all("a", href=re.compile('is2.4chan.org')):
        urls.append(f"https:{img['href']}")
    return list(set(urls))

def get_thread_urls(board):
    blue_boards = ['a','c','g','k','m','o','p','v','vg','vr','w','vip','qa',
                   'cm','lgbt','3','adv','an','asp','biz','cgl','ck','co',
                   'diy','fa','fit','gd','his','int','jp','lit','mlp','mu',
                   'n','out','po','qst','sci','sp','tg','toy','trv','tv',
                   'vp','wsg','wsr','x']
    red_boards  = ['b','d','e','f','gif','h','hr','r','s','t','u','wg','i',
                   'ic','r9k','s4s','hm','y','aco','bant','hc','pol','soc']

    if board in blue_boards:
        domain = 'https://boards.4channel.org'
    elif board in red_boards:
        domain = 'https://boards.4chan.org'
    else:
        raise ValueError('Specified board does not exist.')


    threads = []
    for i in range(10):
        if i == 0:
            page_num = ''
        else:
            page_num = str(i+1)

        page = requests.get(f'{domain}/{board}/{page_num}')
        soup = BeautifulSoup(page.content, 'html.parser')
        page_threads = soup.find_all('a', href = re.compile(f'/thread'))
        page_threads = list(set([x['href'].split('#',1)[0] for x in page_threads]))
        threads.extend([f'{domain}{x}' for x in page_threads])
    
    return threads

def download_image(image_url, directory):
    parse_url = urllib.parse.urlparse(image_url)
    image_name = parse_url.path.rsplit('/',1)[1]
    if os.path.isfile(os.path.join(directory, image_name)):
        return
    request = requests.get(image_url, allow_redirects = True)
    open(os.path.join(directory, image_name), 'wb').write(request.content)

def download_thread_images(thread_url, directory=None):
    if directory is None:
        pictures_dir = os.path.join(os.path.expanduser('~'),'Pictures')
        user_dir = os.path.expanduser('~')
        if os.path.isdir(pictures_dir):
            directory = pictures_dir
        else:
            directory = user_dir

    urls = get_image_urls(thread_url)
    num_urls = len(urls)
    successes = 0
    failures = 0
    for index, url in enumerate(urls):
        print('\rDownloading image {:2} of {:2d} {}'.format(index+1, num_urls, get_bar(index+1, num_urls)), end='', flush = True)
        try:
            download_image(url, directory)
            successes += 1
        except Exception as e:
            print(f'\nError on image url {url}')
            print(f'Exception: [{e}]')
            failures += 1
    print('\rDonwloading image {:2d} of {:2d} {}'.format(num_urls, num_urls, get_bar(num_urls, num_urls)), flush = True)
    print('Finished downloading images.\nSuccesses: {:2d} | Failures: {:2d}'.format(successes, failures))

def get_op_info(thread_url):
    thread = requests.get(thread_url)
    soup = BeautifulSoup(thread.content, 'html.parser')
    for wbr in soup.find_all('wbr'):
        wbr.replace_with('' + wbr.text)
    for br in soup.find_all('br'):
        br.replace_with('\n' + br.text)
    subject = soup.find_all('span', {'class': 'subject'})[1].text
    post = soup.find('blockquote', {'class': 'postMessage'}).text
    return subject, post

def get_bar(index, end):
    if index == 0:
        return '|----------|'
    num_complete = int(index/end*10)
    num_incomplete = 10 - num_complete
    bar = '|'
    for __ in range(num_complete):
        bar += '@'
    for __ in range(num_incomplete):
        bar += '-'
    return (bar+'|')

def main():
    print('Starting scrape - {}'.format(datetime.datetime.now().strftime('%H:%M')))
    board = 'wsg'
    threads = get_thread_urls(board)
    threads = [x for x in threads if x not in exclusions and (x in inclusions or inclusions == [])]
    num_threads = len(threads)
    for index, thread in enumerate(threads):
        subject, post = get_op_info(thread)
        if subject == '':
            subject = thread.rsplit('/', 1)[1]
        directory = os.path.join(os.path.expanduser('~'),'Pictures','4chan','{} - {}'.format(thread.rsplit('/', 1)[1], subject.replace('\\','').replace('/','').replace('"',"'")))
        os.makedirs(directory, exist_ok = True)
        with open(os.path.join(directory,'[OP].txt'), 'w+') as op_file:
            op_file.write(f'Subject\n{subject}\n\nPost\n{post}')
        print('Downloading images for thread {} ({} of {}) [{}]'.format(thread.rsplit('/', 1)[1], index + 1, num_threads, subject))
        download_thread_images(thread,directory)
    print('Finished scrape - {}'.format(datetime.datetime.now().strftime('%H:%M')))

if __name__ == "__main__":
    main()