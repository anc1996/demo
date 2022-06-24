from django.db import models


"""

1.定义模型类
    ① 在哪里定义模型
    ② 模型继承自谁就可以
    ③ ORM对应的关系
        表-->类
        字段-->属性
    2.模型类需要继承自models.Model
    3. 模型类会自动为我们添加(生成)一个主键
    4. 属性名=属性类型(选项)
        属性名: 不要使用 python,mysql关键字
                不要使用 连续的下划线(__)
        属性类型: 和mysql的类型类似的
        选项:  charfiled 必须设置 max_length
                varchar(M)
              null   是否为空
              unique 唯一
              default 设置默认值
              verbose_name 主要是 admin后台显示    
2.模型迁移
    2.1 先生成迁移文件(不会在数据库中生成表,只会创建一个数据表和模型的对应关系)
        python manage.py makemigratons
    2.2 再迁移(会在数据库中生成表)
        python manage.py migrate
3.操作数据库

"""

# Create your models here.
class BookInfo(models.Model):
    """
     1.主键 当前会自动生成
     2.属性复制过来就可以
     """
    """
    书籍表:
        id,name,pub_date,readcount,commentcount,is_delete
    """
    #默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。
    # 属性名=属性类型(选项)
    name=models.CharField(max_length=10,unique=True,verbose_name='名字')
    # 发布日期
    pub_date=models.DateField(null=True,verbose_name='发布日期')
    # 阅读量
    readcount=models.IntegerField(default=0,verbose_name='阅读量')
    # 评论量
    commentcount=models.IntegerField(default=0,verbose_name='评论量')
    # 是否逻辑删除
    is_delete=models.BooleanField(default=False,verbose_name='书是否删除')

    #自动为我们添加一个属性，这个属性可以通过书籍查询人物信息。
    class Meta:
        db_table='bookinfo' # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称

    def __str__(self):
        """将模型类以字符串的方式输出"""
        return self.name

# 准备人物列表信息的模型类
class PeopleInfo(models.Model):
    # 有序字典
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )


    # 一个黑帮老大 n个小弟 1:n
    # 黑帮老大被判死刑
    # 小弟:   1. 劫狱 不让老大死
    #         2.  小弟自己混
    #          3. 老大死 小弟跟着死

    # 书籍: 人物  1:n
    # 西游记:  孙悟空,白骨精
    # on_delete
    name = models.CharField(max_length=20, verbose_name='名称')
    gender=models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='他是否删除')

    class Meta:
        db_table = 'peopleinfo' # 指明数据库表名,模型类如果未指明表名，Django默认以小写app应用名_小写模型类名为数据库表名。
        verbose_name = '人物信息' # 在admin站点中显示的名称

    def __str__(self):
        """将模型类以字符串的方式输出"""
        return self.name