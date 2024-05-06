from django.db import models
# CharField对应于MySQL中的VARCHAR。unique=True用于指定该字段的值在数据库中是唯一的。
# EmailField是Django提供的特殊字段，会验证电子邮件地址的有效性。
# unique_together用于指定在数据库中联合唯一性约束。

# Django项目中的settings.py文件，找到DATABASES设置部分，并进行如下配置：
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'CSshop',
#         'USER': '数据库用户，我猜是root',
#         'PASSWORD': '数据库密码',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # 单一主键
    steam_id = models.CharField(max_length=30, unique=True)
    picture = models.CharField(max_length=255)
    username = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    # example = models.CharField(default=5) # 不想要的字段注释掉重新运行makemigrations两步即可
    # PS: 如果要加入字段则会面临两个选择，选1随后输入默认值
    # 选2则退出，需要给字段加默认值，如上方的example      或者直接默认空值（不建议）

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    identifier = models.CharField(max_length=10)

# 在terminal中先输入：python manage.py makemigrations（无法运行则输入python当前版本如python3.7）
# 再输入python manage.py migrate      PS:这两步操作需要在项目根目录进行

# 添加数据
# Transaction.objects.create(income="50",expense="20",price="30",identifier="收益")