from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)  # 自增用户编号
    user_class = models.CharField(max_length=50)  # 班级
    studentid = models.CharField(max_length=20, unique=True)  # 学号
    name = models.CharField(max_length=50)  # 学生姓名
    teamname = models.CharField(max_length=50)  # 队名
    pwd = models.CharField(max_length=50)  # 密码
    phone = models.CharField(max_length=15)  # 电话
    group = models.IntegerField()  # 组号
    number = models.IntegerField()  # 企业编号

    def __str__(self):
        return f"{self.studentid} ({self.name})"
