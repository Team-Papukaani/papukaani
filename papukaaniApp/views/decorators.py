import logging
import queue
from papukaaniApp.utils.view_utils import ALL_METHOD_NAMES


def count_lajistore_requests(old_view):
    def new_view(request, *args, **kwargs):
        summary_logger = logging.getLogger(
            'papukaaniApp.lajistore_requests_summary')
        full_logger = logging.getLogger('papukaaniApp.lajistore_requests')

        q = queue.Queue()
        h = logging.handlers.QueueHandler(q)
        requests_logger = logging.getLogger('requests.packages.urllib3')
        requests_logger.addHandler(h)
        requests_logger.setLevel('DEBUG')
        assert q.qsize() == 0

        response = old_view(request, *args, **kwargs)

        num_requests = 0
        while q.qsize() > 0:
            r = q.get()
            word_1 = r.msg.strip('"').split(' ', 1)[0]
            if word_1 in ALL_METHOD_NAMES:
                full_logger.info('Made request: %s' % r.msg.strip('"'))
                num_requests += 1

        msg = 'Made %s requests while serving %s' % (str(num_requests),
                                                     request.get_full_path())
        summary_logger.info(msg)
        requests_logger.removeHandler(h)

        return response

    return new_view
