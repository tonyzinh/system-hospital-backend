from django.db import models

class KnowledgeDocument(models.Model):
    source_url = models.URLField(max_length=500, unique=True)
    title = models.CharField(max_length=300, blank=True)
    text = models.TextField()  # conteúdo limpo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.source_url
