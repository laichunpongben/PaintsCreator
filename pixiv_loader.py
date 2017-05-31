from __future__ import print_function
import os
import sys
import json
import time
import pixivpy3
if sys.version_info >= (3, 0):
    import pickle
else:
    import cPickle as pickle
import numpy as np
from PIL import Image


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
        result = self.users_works(artist_id, per_page=1000)
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
        illust_count = 0
        for illust in self.generate_illust(artist_id):
            aapi.download(illust.image_urls.large, fpath)
            print('Saving {}'.format(illust.id))
            illust_count += 1
            time.sleep(self.DOWNLOAD_DELAY)

        print('Total {} illusts saved'.format(illust_count))

    def make_thumbnail(self, infile):
        size = 128, 128
        outfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'thumbnails',
                              os.path.splitext(os.path.basename(infile))[0] +
                              '.thumbnail' +
                              os.path.splitext(os.path.basename(infile))[1])
        try:
            image = Image.open(infile)
            image.thumbnail(size, Image.ANTIALIAS)
            background = Image.new('RGBA', size, (255, 255, 255, 0))
            background.paste(
                image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
            )
            background.save(outfile, "JPEG")
        except IOError:
            raise

    def make_dataset(self):
        image_ext = ['.jpg', '.png', '.gif']
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         'illusts')):
            for f in files:
                if f.endswith(tuple(image_ext)):
                    self.make_thumbnail(os.path.join(root, f))

    def serialize(self):
        np.savez('pixiv.npz', x, y)

    def load_data(self):
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'datasets',
                             'pixiv.npz')
        try:
            f = np.load(path)
            x_train = f['x_train']
            y_train = f['y_train']
            x_test = f['x_test']
            y_test = f['y_test']
        finally:
            f.close()
        return (x_train, y_train), (x_test, y_test)

if __name__ == '__main__':
    artist_id = 946272
    pixiv_loader = PixivLoader()
    # pixiv_loader.save_illusts(artist_id)
    pixiv_loader.make_dataset()
