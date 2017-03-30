"""
Implement action to iteract with database
"""
import zerodb
import transaction
from models import Posts
import config
import log

CONF = config.get_config()
LOG = log.setup_log("My-Blog")


class ZeroDBStorage(object):
    def __init__(self):
        """
        Init variables
        """
        self.username = CONF.get('zerodb', 'username')
        self.password = CONF.get('zerodb', 'password')
        self.host = CONF.get('zerodb', 'host')
        self.port = int(CONF.get('zerodb', 'port'))
        self.db = zerodb.DB((self.host, self.port),
                            username=self.username,
                            password=self.password)

    def _create(self, post):
        with transaction.manager:
            try:
                post_id = 0
                posts = self.db[Posts].query(table_role="post")
                if len(posts) != 0:
                    post_id = int(posts[len(posts)-1].post_id) + 1
                p = Posts(post_id=post_id,
                          post_title=post['title'],
                          post_content=post['content'],
                          table_role="post")
                self.db.add(p)
                return True
            except:
                LOG.error("Cannot create a post")
        self.db.disconnect

    def _delete(self, post):
        try:
            post_record = self.db[Posts].query(post_id=int(post['post_id']))
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a post "
                      "with post ID: %s" % post['post_id'])

    def _get(self):
        try:
            posts = self.db[Posts].query(table_role="post")
            LOG.debug("Posts: " + str(list(posts)))
            return list(posts)
        except Exception as e:
            LOG.error("Cannot get posts in database: %s" % e)
