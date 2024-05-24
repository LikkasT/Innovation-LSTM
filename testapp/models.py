from datetime import timedelta
from django.db import models
from django.db.models import F, Subquery, OuterRef, Case, When, Value, DecimalField


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
# 饰品大类
class JewelryType(models.Model):
    jewelry_id = models.AutoField(primary_key=True)
    wear_and_tear = models.CharField(max_length=50,null=True, blank=True) # 磨损度，可空
    image = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=50)
# 用户表
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=64)
    steam_id = models.CharField(max_length=30)
    image = models.CharField(max_length=255)
    username = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    # 添加一个多对多字段，连接到JewelryType
    favorite_jewelry_types = models.ManyToManyField(JewelryType, through='FavoriteJewelry')
    # example = models.CharField(default=5) # 不想要的字段注释掉重新运行makemigrations两步即可
    # PS: 如果要加入字段则会面临两个选择，选1随后输入默认值
    # 选2则退出，需要给字段加默认值，如上方的example      或者直接默认空值（不建议）


class JewelryManager(models.Manager):
    def with_price_increase(self, days):
        # 定义包含价格涨幅计算的 QuerySet
        return self.annotate(
            price_increase=Case(
                When(
                    past_price__gt=0,
                    then=(F('price') - Subquery(
                        self.model.objects.filter(
                            jewelry_id=OuterRef('jewelry_id'),
                            created_at__lte=F('created_at') - timedelta(days=days)
                        ).values('price')[:1]
                    )) / Subquery(
                        self.model.objects.filter(
                            jewelry_id=OuterRef('jewelry_id'),
                            created_at__lte=F('created_at') - timedelta(days=days)
                        ).values('price')[:1]
                    ) * Value(100)
                ),
                default=Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).order_by('price_increase')


# 中间模型，用来存储额外的信息
class FavoriteJewelry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 删除上级目录则本目录直接删除
    jewelry_type = models.ForeignKey(JewelryType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # 自动记录当前收藏时间

    class Meta:
        # 设置联合主键，确保一个用户不会收藏同一种饰品类型多次
        unique_together = ('user', 'jewelry_type')

# 交易表
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    identifier = models.CharField(max_length=10)
    # 外键为用户
    user = models.ForeignKey(to="User",to_field="user_id",null=True,blank=True,on_delete=models.SET_NULL)
    # 可为null且删除用户后user置空
    jewelry_type = models.ForeignKey(to='JewelryType',to_field="jewelry_id",null=True,blank=True,on_delete=models.SET_NULL)


# 饰品小类
class Jewelry(models.Model):
    small_jewelry_id = models.AutoField(primary_key=True)
    date = models.DateTimeField() # 日期时间
    price = models.DecimalField(max_digits=10, decimal_places=2)
    units_sold = models.IntegerField()  # 在售数
    # 外键为饰品大类id
    jewelry_id = models.ForeignKey(to="JewelryType", to_field="jewelry_id", null=True, blank=True, on_delete=models.SET_NULL)
    # 可为null且删除饰品后jewelry_id置空
    objects = JewelryManager()



# 添加数据
# Transaction.objects.create(income="50",expense="20",price="30",identifier="收益")
@property
def price_increase(self, days):
    days_ago = self.created_at - timedelta(days=days)
    try:
        past_price = Jewelry.objects.get(created_at__lte=days_ago, jewelry_id=self.jewelry_id).price
        if past_price == 0:
            return 0
        return (self.price - past_price) / past_price * 100
    except Jewelry.DoesNotExist:
        return None
