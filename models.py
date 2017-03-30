from zerodb.models import Model, Field, Text


class Posts(Model):
    """
    Model for Posts table
    """
    post_id = Field()
    post_title = Field()
    post_content = Text()
    table_role = Field()

    def __repr__(self):
        return str({"post_id": self.post_id,
                    "post_title": self.post_title,
                    "post_content": self.post_content,
                    "table_type": self.table_role})
