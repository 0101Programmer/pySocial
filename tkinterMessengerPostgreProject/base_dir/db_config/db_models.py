import tortoise.fields
from tortoise.models import Model


class Dialog(Model):
    id = tortoise.fields.IntField(pk=True)
    started_by_user = tortoise.fields.ForeignKeyField("app.User", related_name="dialogs_started_by_user")
    second_user = tortoise.fields.ForeignKeyField("app.User", related_name="dialogs_started_with_user", null=True)
    dialog_data = tortoise.fields.JSONField()
    total_messages = tortoise.fields.IntField(default=1)
    last_message_time = tortoise.fields.DatetimeField(auto_now=True)


class User(Model):
    id = tortoise.fields.IntField(pk=True)
    email = tortoise.fields.CharField(max_length=100, unique=True)
    password = tortoise.fields.CharField(max_length=100)
    name = tortoise.fields.CharField(max_length=100)
    birthdate = tortoise.fields.DateField()
    profile_pic_path = tortoise.fields.CharField(max_length=100, default='../static/profile_pics/default_profile.png')
    optional_data = tortoise.fields.JSONField(null=True)
    session_data = tortoise.fields.JSONField()
    created_at = tortoise.fields.DatetimeField(auto_now_add=True)
    updated_at = tortoise.fields.DatetimeField(auto_now=True)
    friends = tortoise.fields.JSONField(null=True)
    dialogs_started_by_user: tortoise.fields.BackwardFKRelation[Dialog]
    dialogs_started_with_user: tortoise.fields.BackwardFKRelation[Dialog]

class Phone(Model):
    id = tortoise.fields.IntField(pk=True)
    model = tortoise.fields.CharField(max_length=100)
    person = tortoise.fields.ForeignKeyField("app.Person", related_name="phones")


class Person(Model):
    id = tortoise.fields.IntField(pk=True)
    name = tortoise.fields.CharField(max_length=100)
    phones: tortoise.fields.BackwardFKRelation[Phone]