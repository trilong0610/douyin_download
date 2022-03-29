from django.db import models


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    id_video = models.CharField(max_length=255, null=True, blank=True);
    sec_uid = models.CharField(max_length=255,null=True, blank=True);

    def __str__(self):
        return str(self.id_video)