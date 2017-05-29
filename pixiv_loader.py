from __future__ import print_function
import os
import json
import time
import pixivpy3


class PixivLoader(pixivpy3.PixivAPI):
    DOWNLOAD_DELAY = 2

    def __init__(self):
        super(PixivLoader, self).__init__()
        self._auth()

    def _auth(self):
        with open('client.json', 'r') as client_json:
            client_info = json.load(client_json)
        self.login(client_info['id'], client_info['pwd'])

    def generate_illust(self, artist_id):
        result = self.users_works(artist_id)
        with open('artist.json', 'w') as artist_json:
            json.dump(result, artist_json)

        for i in range(result.count):
            yield result.response[i]

    def save_illusts(self, artist_id):
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'illusts',
                             str(artist_id),
                             '')
        if not os.path.exists(fpath):
            os.mkdir(fpath)

        aapi = pixivpy3.AppPixivAPI()
        for illust in self.generate_illust(artist_id):
            aapi.download(illust.image_urls.large, fpath)
            time.sleep(self.DOWNLOAD_DELAY)

        print('Illusts saved')

if __name__ == '__main__':
    artist_id = 4889903
    pixiv_loader = PixivLoader()
    pixiv_loader.save_illusts(artist_id)
