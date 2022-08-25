from pybooru import Danbooru
from tqdm import tqdm
import os
import requests


def parse(query, page, limit):
    query = '_'.join(query.split())
    client = Danbooru('danbooru')
    posts = client.post_list(tags=query, page=page, limit=limit)

    results = []

    if not os.path.isdir(query):
        os.mkdir(query)
    for post in tqdm(posts):
        url = ''
        if post['file_ext'] in ('jpg', 'png'):
            if 'source' in post.keys():
                url = post['source']
            else:
                if post['has_large']:
                    url = post['large_file_url']
                else:
                    url = post['file_url']
            if url:
                try:
                    resp = requests.get(url)
                except requests.exceptions.SSLError as e:
                    if post['has_large']:
                        url = post['large_file_url']
                    else:
                        url = post['file_url']
                    resp = requests.get(url)
                if resp.status_code == 200:
                    filename = '{}/{}.{}'.format(query,
                                                 post['id'], post['file_ext'])
                    try:
                        with open(filename, 'wb') as out:
                            out.write(resp.content)
                            results.append(filename)
                    except IOError:
                        pass
    return results


if __name__ == '__main__':
    parse(input('> '))
