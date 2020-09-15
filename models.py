from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors={}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['password']) <8:
            errors['password'] = "Your password must be a least 8 characters"
        if len(postdata['first_name']) <2:
            errors['first_name'] = "Your first name must be a least 2 characters"
        if len(postdata['last_name']) <2:
            errors['last_name'] = "Your last name must be a least 2 characters"
        if not email_checker.match(postdata['email']):
            errors['email'] = "Your email is invalid"
        if postdata['password'] != postdata['confirm_password']:
            errors['password'] = "Password and Confirm Password don't match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=50)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Age_Range(models.Model):
    tier1 = 't1'
    tier2 = 't2'
    tier3 = 't3'
    tier4 = 't4'
    tier5 = 't5'
    tier6 = 't6'
    tier7 = 't7'
    tier8 = 't8'
    tier9 = 't9'
    
    AGE_CHOICES = (
        (tier1, 't1'),
        (tier2, 't2'),
        (tier3, 't3'),
        (tier4, 't4'),
        (tier5, 't5'),
        (tier6, 't6'),
        (tier7, 't7'),
        (tier8, 't8'),
        (tier9, 't9'),
    )
    # age_range_client = models.CharField(max_length=2, choices=AGE_CHOICES,default=tier5)
    # first_name = models.CharField(max_length=25)
    # last_name = models.CharField(max_length=50)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class Risk(models.Model):
    very_low = 'r1'
    low= 'r2'
    medium = 'r3'
    aggressive = 'r4'
    high = 'r5'
    RISK_CHOICES = (
        (very_low, 'r1'),
        (low, 'r2'),
        (medium, 'r3'),
        (aggressive, 'r4'),
        (high, 'r5'),
    )
    risk_range_client = models.CharField(max_length=2, choices=RISK_CHOICES,default=medium)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)