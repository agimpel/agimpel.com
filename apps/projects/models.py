from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='projects')

    github_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='projects', blank=True, null=True)

    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def print_tags(self):
        return ', '.join([tag.name for tag in self.tags.all()])