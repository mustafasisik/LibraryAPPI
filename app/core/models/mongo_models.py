from djongo import models as mongo_models


class Log(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    message = mongo_models.TextField(max_length=1000)

    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        _use_db = 'nonrel'
        ordering = ("-created_at", )

    def __str__(self):
        return self.message


class Book(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    barcode = mongo_models.CharField(max_length=7)
    name = mongo_models.TextField(max_length=100)
    is_reserved = mongo_models.BooleanField(default=False)
    is_deleted = mongo_models.BooleanField(default=False)
    user_id = mongo_models.IntegerField(default=0)
    return_date = mongo_models.DateTimeField(default=None, null=True)
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        _use_db = 'nonrel'
        ordering = ("-created_at", "name" )

    def __str__(self):
        return str(self._id)
