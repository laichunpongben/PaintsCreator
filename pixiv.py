import pixivpy3

if __name__ == '__main__':
    api = pixivpy3.AppPixivAPI()
    json_result = api.illust_detail(59580629)
    illust = json_result.illust
    print(">>> origin url: %s" % illust.image_urls['large'])
