from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.models_LajiStore import individual


class News:
    '''
    Represents the News table of LajiStore
    '''

    def __init__(self, title, content, language, publishDate=None, targets=None, id=None, **kwargs):
        self.title = title
        self.content = content
        self.language = language
        self.publishDate = publishDate
        self.targets = set() if targets is None else targets
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
        Attaches this piece of news to an individual. Note always cleans up existing individuals that have been deleted
        :returns True if attached or previously attached. False if attachment failed because individual didn't exist
        '''
        self.targets.add(individualid)
        self._cleanup_deleted_individuals()
        self.update()
        return individualid in self.targets

    def detach_from(self, individualid):
        '''
        Removes this piece of news from an individual. Always does cleanup
        :returns True if was previously attached and was removed. False if was not attached previously
        '''
        remove = False
        if individualid in self.targets:
            remove = True
            self.targets.remove(individualid)
        self._cleanup_deleted_individuals()
        self.update()
        return remove

    def get_attached_individuals(self):
        '''
        Return currently attached individuals ids
        :return: Set
        '''
        return self.targets

    def is_attached(self):
        return True if self.get_attached_individuals() else False

    def _cleanup_deleted_individuals(self):
        '''
        Removes softdeleted and deleted individuals from local targets
        '''
        birds = individual.find_exclude_deleted()
        valid = set()
        for bird in birds:
            if bird.id in self.targets:
                valid.add(bird.id)
        self.targets = valid


def find_by_individual_and_language(individualID, language):
    '''
    Find all matching news for the individual.
    :param individualid:
    :return: list of news
    '''
    individualID = '"' + LajiStoreAPI._URL + LajiStoreAPI._INDIVIDUAL_PATH + '/' + individualID + '"'

    return find(targets=individualID, language=language)


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
    if 'id' in news:
        return News(**news)
    else:
        return None


def create(title, content, language, publishDate=None, targets=None):
    '''
    Creates a news instance in LajiStore and a corresponding News object
    :return: A News object
    '''
    try:
        news = News(title, str(content).strip(), language, publishDate, targets)
        data = LajiStoreAPI.post_news(**news.__dict__)
        news.id = data['id']
    except Exception as e:
        raise Exception("Error saving data")

    return news


def delete_all():
    '''
    Deletes all news. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_news()
