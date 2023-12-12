from django.db import models


class RodDocument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="roddocuments/")

    @classmethod
    def create_document(cls, name, file):
        new_document = cls(name=name, file=file)
        new_document.save()
        return new_document

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete()
        super().delete(*args, **kwargs)
