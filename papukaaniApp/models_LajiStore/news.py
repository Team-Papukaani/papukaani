from papukaaniApp.services.lajistore_service import LajiStoreAPI


class News:
    '''
    Represents the News table of LajiStore
    '''

    def __init__(self, title, content, language, publishDate=None, targets=[], id=None, **kwargs):
        self.title = title
        self.content = content
        self.language = language
        self.publishDate = publishDate
        self.targets = targets
        self.id = id

    def delete(self):
        '''
        Deletes the news from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_news(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''
        LajiStoreAPI.update_news(**self.__dict__)  # __dict__ puts all arguments here.

    def attach_to(self, individualid):
        '''
        Attaches this piece of news to an individual
        '''
        raise NotImplementedError

    def detach_from(self, individualid):
        '''
        Removes this piece of news from an individual
        '''
        raise NotImplementedError

    def get_attached_individuals(self):
        '''
        Return currently attached individuals ids
        :return: List
        '''
        return []

    def is_attached(self):
        return True if self.get_attached_individualid() else False


def find(**kwargs):
    '''
    Find all matching news.
    :param kwargs: Search parameters. No parameters will search all news.
    :return: A list of News objects.
    '''
    data = LajiStoreAPI.get_all_news(**kwargs)
    news = []
    for n in data:  # Creates a list of news to return
        news.append(News(**n))
    return news


def get(id):
    '''
    Gets a piece of news from LajiStore
    :param id: The LajiStore ID of the news
    :return: A news object
    '''

    news = LajiStoreAPI.get_news(id)
    if '@id' in news:
        return News(**news)
    else:
        return None


def create(title, content, language, publishDate=None, targets=[]):
    '''
    Creates a news instance in LajiStore and a corresponding News object
    :return: A News object
    '''

    news = News(title, content, language, publishDate, targets)
    data = LajiStoreAPI.post_news(**news.__dict__)

    news.id = data['id']

    return news


def delete_all():
    '''
    Deletes all news. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_news()
