from zerodb.models import Model, Field, Text


class Posts(Model):
    """
    Model for Posts table
    """
    pid = Field()
    post_title = Field()
    post_content = Text()
    table_role = Field()

    def __repr__(self):
        return str({"pid": self.pid,
                    "post_title": self.post_title,
                    "post_content": self.post_content,
                    "table_role": self.table_role})
