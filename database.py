"""
Implement action to iteract with database
"""
import zerodb
import transaction
from models import Posts
import config
import log

import uuid
CONF = config.get_config()
LOG = log.setup_log("My-Blog")


class ZeroDBStorage(object):
    def __init__(self):
        """
        Init variables
        Read zerodb config from file
        """
        self.username = CONF.get('zerodb', 'username')
        self.password = CONF.get('zerodb', 'password')
        self.host = CONF.get('zerodb', 'host')
        self.port = int(CONF.get('zerodb', 'port'))
        self.db = zerodb.DB((self.host, self.port),
                            username=self.username,
                            password=self.password)

    def _create(self, post):
        """
        Create a post
        """
        with transaction.manager:
            try:
                pid = str(uuid.uuid4())
                p = Posts(pid=pid,
                          post_title=post['title'],
                          post_content=post['content'],
                          table_role="post")
                self.db.add(p)
                return True
            except:
                LOG.error("Cannot create a post")
        self.db.disconnect

    def _delete(self, post_id):
        try:
            post_record = self.db[Posts].query(pid=post_id)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a post "
                      "with post ID: %s" % post['pid'])

    def _get(self, pid=None):
        try:
            if pid is None:
                posts = self.db[Posts].query(table_role="post")
                LOG.debug("Posts: " + str(list(posts)))
                return list(posts)
            else:
                post = self.db[Posts].query(table_role="post",
                                            pid=pid)
                LOG.debug("Post: " + str(list(post)))
                return list(post)
        except Exception as e:
            LOG.error("Cannot get posts in database: %s" % e)
