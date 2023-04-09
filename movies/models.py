from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.CharField(
        max_length=11,
        choices=[('Male','Male'),('Female','Female'),('Other','Other')]
    )
    def __str__(self):
        return self.user.username

# Create your models here.
class Views(models.Model):
    m_id=models.PositiveIntegerField(primary_key = True)
    sum=models.IntegerField()
    count=models.PositiveIntegerField()
    def __str__(self):
        return str(self.m_id) + ", " + str(self.sum) + ", " + str(self.count)


class Ratings(models.Model):
    ron=models.ForeignKey(Views,db_column='ron', on_delete=models.CASCADE)
    rby=models.ForeignKey(Users,db_column='rby', on_delete=models.CASCADE)
    rating=models.FloatField()
    rorb_id=models.AutoField(primary_key = True)
    class Meta:
        unique_together = (("ron", "rby"))
    def __str__(self):
        return  str(self.ron.m_id) + ", " + self.rby.user.username +", " + str(self.rating)


class Cat_list(models.Model):
    category=models.CharField(max_length=30,primary_key = True)
    def __str__(self):
        return self.category

class Lang_list(models.Model):
    language=models.CharField(max_length=30,primary_key = True)
    def __str__(self):
        return self.language
    

class Catalog(models.Model):
    id=models.PositiveIntegerField(primary_key= True)
    person=models.CharField(max_length=30)
    portrait = models.CharField(max_length=200,default="https://i.pinimg.com/564x/e3/82/55/e38255b8fad2209e3f0252e8b4ba0612.jpg")
    def __str__(self):
        return self.person


class Movie(models.Model):
    m_id=models.PositiveIntegerField(primary_key= True)
    m_name=models.CharField(max_length=50)
    release_year=models.PositiveIntegerField()
    rating=models.FloatField(null=True, blank=True)
    studio=models.CharField(max_length=30)
    ageplus=models.PositiveIntegerField()
    run_time=models.TimeField()
    portrait = models.CharField(max_length=200,default="https://i.pinimg.com/564x/e3/82/55/e38255b8fad2209e3f0252e8b4ba0612.jpg")
    landscape = models.CharField(max_length=200,default="https://wallpapercave.com/wp/wp7955488.jpg")
    def __str__(self):
        return str(self.m_id) + ", " + self.m_name


class Categories(models.Model):
    c_id=models.AutoField(primary_key = True)
    m_id=models.ForeignKey(Movie, db_column='m_id',on_delete=models.CASCADE)
    category=models.ForeignKey(Cat_list,db_column='category', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("m_id", "category"))
    def __str__(self):
        return self.m_id.m_name + ", " + self.category.category

class Languages(models.Model):
    l_id=models.AutoField(primary_key = True)
    m_id=models.ForeignKey(Movie, db_column='m_id',on_delete=models.CASCADE)
    language=models.ForeignKey(Lang_list,db_column='language', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("m_id", "language"))
    def __str__(self):
        return self.m_id.m_name + ", " + self.language.language

class Actor(models.Model):
    a_id=models.AutoField(primary_key = True)
    m_id=models.ForeignKey(Movie, db_column='m_id',on_delete=models.CASCADE)
    actor_id=models.ForeignKey(Catalog,db_column='actor_id', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("m_id", "actor_id"))
    def __str__(self):
        return self.m_id.m_name + ", " + self.actor_id.person

class Actress(models.Model):
    a_id=models.AutoField(primary_key = True)
    m_id=models.ForeignKey(Movie, db_column='m_id',on_delete=models.CASCADE)
    actress_id=models.ForeignKey(Catalog,db_column='actress_id', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("m_id", "actress_id"))
    def __str__(self):
        return self.m_id.m_name + ", " + self.actress_id.person

class Director(models.Model):
    d_id=models.AutoField(primary_key = True)
    m_id=models.ForeignKey(Movie, db_column='m_id',on_delete=models.CASCADE)
    director_id=models.ForeignKey(Catalog,db_column='director_id', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("m_id", "director_id"))
    def __str__(self):
        return self.m_id.m_name + ", " + self.director_id.person

class Contact(models.Model):
    c_id=models.PositiveIntegerField()
    customer=models.CharField(max_length=150)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.CharField(max_length=254)
    reason=models.CharField(max_length=500)
    at=models.DateTimeField()
    number=models.CharField(max_length=16)
    def __str__(self):
        return  self.first_name + " " +  self.last_name +" (" + self.customer +")"