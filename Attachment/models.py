from django.db import models
from django.utils import timezone
from Post.models import Post


# Create your models here.
class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'<Attachment: {self.name}>'
