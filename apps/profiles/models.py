from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    research_interests = models.JSONField(default=list, blank=True)
    avatar = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    google_scholar = models.URLField(blank=True, null=True)
    researchgate = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

    @property
    def followers_count(self):
        return self.user.followers.count()

    @property
    def following_count(self):
        return self.user.following.count()

    @property
    def projects_count(self):
        return self.user.projects.count()

    @property
    def publications_count(self):
        return self.user.authored_publications.count()

    def __str__(self):
        return f"{self.user.full_name}'s Profile"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        unique_together = ['follower', 'following']

    def __str__(self):
        return f"{self.follower.full_name} follows {self.following.full_name}"
