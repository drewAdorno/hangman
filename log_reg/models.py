from django.db import models

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors={}
        if '@' not in postData['email'] or '.' not in postData['email']:
            errors['email']= 'Invalid Email'
        if len(postData['password'])<8:
            errors['password']= 'Password needs to be at least 8 characters'
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email must be unique."
        if len(User.objects.filter(username=postData['username'])) > 0:
            errors['username'] = "Username must be unique."
        if postData['password'] != postData['confirmPassword']:
            errors['password']= 'Password and Confirm Password do not match'
        return errors
    def loginValidator(self, postData):
        errors={}
        if len(User.objects.filter(email=postData['usernameEmail'])) or len(User.objects.filter(username=postData['usernameEmail']))== 0:
            errors['usernameEmail'] = "Email or Username does not exist"
            return errors
        user= User.objects.filter(email=postData['usernameEmail'], username=postData['usernameEmail'])  #check that this query works
        if user[0].password != postData['password']:
            errors['password']= 'Incorrect Email/Password combination'
        return errors
class User(models.Model):
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    objects=UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<User object: {self.username}, {self.email}>"
