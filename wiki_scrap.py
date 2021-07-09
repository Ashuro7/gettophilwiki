import re
import requests
from bs4 import BeautifulSoup

wiki_base_url = 'https://en.wikipedia.org/wiki/'

def links_para(topic, idx) -> str:
    
    url = wiki_base_url + topic
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
        return None

    avd_ext = [r'\.', r'Help:', r':', r'#']

    btsoup = BeautifulSoup(page.content, 'html.parser')
    
    hrefs = []
    wiki_list = []
    paras = [x for x in btsoup.find_all("p")]
    
    for i in range(len(paras)):
        hrefs = [a.get('href') for a in paras[i]("a")]

        if len(hrefs) > 0 and None not in hrefs:
            for i in hrefs:
                if re.match(r'^/wiki', i) and not re.search(r'|'.join(avd_ext), i, re.IGNORECASE):
                    wiki_list.append(i)
            hrefs.clear()    
    
    if idx < len(wiki_list):
        first_topic = wiki_list[idx]
        pattern = re.compile(r'/')

        l = list(pattern.finditer(first_topic))[-1].span()[0]
        return first_topic[l+1:]
    else:
        print('Index out of bound for Wiki_List')
    

def wiki_scrap(inittopic):
    topic = inittopic

    f = open(inittopic+'.txt', 'w+')
    count = 0
    visited = []

    while count < 100:

        visited.append(topic)
        print(topic)
        f.write(str(topic)+'\n')

        if topic == 'Philosophy':
            print('Philosophy Found')
            break

        try:
           idx = 0
           prev = topic
           topic = links_para(topic, idx)
           if topic is None:
               return 
           while topic in visited:
               idx = idx + 1
               topic = links_para(prev, idx)

        except Exception as e:
            print(e)
        
        count = count + 1
    f.close()

if __name__ == '__main__':
    wiki_scrap(inittopic='Osmosis');




