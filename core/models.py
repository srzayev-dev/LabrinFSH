from django.db import models
from LabrinFSH.utils.base import BaseModel

class Post(BaseModel):
    title = models.CharField(max_length=255, verbose_name="title of the File")
    desc = models.TextField(verbose_name="description")
    file_field = models.FileField(upload_to='files')
    user = models.ForeignKey(
        'users.User', 
        verbose_name="User",
        related_name="postOfUser",
        on_delete=models.CASCADE, null=True, blank=True 
    )

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
    
    def __str__(self):
        return f'{self.title}'

class SharePost(BaseModel):
    file = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shareposts", verbose_name="Share Post")
    user = models.ForeignKey(
        'users.User', 
        verbose_name="User",
        related_name="postUser",
        on_delete=models.CASCADE, null=True, blank=True 
    )
    sharedUser = models.ForeignKey(
        'users.User', 
        verbose_name="Shared User",
        related_name="sharedPostOfUser",
        on_delete=models.CASCADE, null=True, blank=True 
    )
    can_see = models.BooleanField(default=True)
    can_comment = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "sharedUser")

    def save(self, *args, **kwargs):
        if self.user == self.sharedUser:
            raise ValueError("User cannot share with himself")
        super().save(*args, **kwargs)
        
