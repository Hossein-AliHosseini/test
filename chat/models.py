from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from account.models import CustomUser


# class Message(models.Model):
#     username = models.CharField()
#     room = models.CharField(max_length=255)
#     content = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('date_added',)


class Message(models.Model):
    room = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # replied_to = models.ForeignKey('chat.Message',
    #                                on_delete=models.CASCADE,
    #                                null=True)

    class Meta:
        ordering = ('date_added',)
    """
    for retrieving data:

    1.
    Get the 'ContentType' object with the following code.
    from django.contrib.contenttypes.models import ContentType
    contenttype_obj = ContentType.objects.get_for_model(project_object)

    2.
    "object_id" is stored with project_object.id
    TimeLine.objects.filter(object_id=project_object.id, content_type=contenttype_obj)
    """
