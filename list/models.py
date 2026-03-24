from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_time:
            raise ValueError("End time is required")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Untitled Todo"


class Category(models.Model):
    todo = models.ForeignKey(
        Todo,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name