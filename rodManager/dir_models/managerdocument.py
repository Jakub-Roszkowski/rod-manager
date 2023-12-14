from django.db import models


class ManagerDocument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="managerdocuments/", null=True, blank=True)

    def to_dict(self):
        result = {"id": self.id, "name": self.name}
        if self.file:
            result["file_url"] = "/" + self.file.name
        children = self.children.all()
        if children:
            result["items"] = [child.to_dict() for child in children]
        return result

    @classmethod
    def create_document(cls, name, parent=None, file=None):
        new_document = cls(name=name, parent=parent, file=file)
        new_document.save()
        return new_document

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete()
        for child in self.children.all():
            child.delete()
        super().delete(*args, **kwargs)
