from zerodb.models import Model, Field, Text


class Posts(Model):
    """
    Model for Posts table
    """
    post_id = Field()
    post_title = Field()
    post_content = Field()
    # owner_id = Field()


class Users(Model):
    """
    Model for users table
    """
    user_id = Field()
    user_name = Field()
    user_password = Field()
