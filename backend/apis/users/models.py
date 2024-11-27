from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo 
# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)  # 自增用户编号
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')  # 学号
    password = models.CharField(max_length=128, verbose_name='密码')  # 密码，加密
    name = models.CharField(max_length=50, verbose_name='学生姓名')  # 学生姓名
    user_class = models.CharField(max_length=50, verbose_name='班级')  # 班级
    team_name = models.CharField(max_length=50, verbose_name='队名')  # 队名
    #email = models.EmailField(unique=True, verbose_name='邮箱')  # 邮箱，唯一约束
    phone = models.CharField(max_length=15, verbose_name='电话')  # 电话
    group = models.IntegerField(verbose_name='组号')  # 组号
    number = models.IntegerField(verbose_name='企业编号')  # 企业编号
    register_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')  # 注册时间
    rest_rounds = models.IntegerField(null=True,blank=True,verbose_name='剩余重开机会')  # 剩余重开机会


    def __str__(self):
        return f"{self.uid} ({self.name})"
    



class Round(models.Model):
    # 自定义的 round_id，可以使用 CharField，并设置 unique=True
    round_id = models.CharField(max_length=50, primary_key=True, verbose_name='轮次编号')

    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户编号')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    def save(self, *args, **kwargs):
        if not self.round_id:
            # 定义北京时间时区
            beijing_tz = ZoneInfo('Asia/Shanghai')
            # 将 start_time 转换为北京时间
            beijing_time = self.start_time.astimezone(beijing_tz)
            # 生成北京时间的时间戳
            timestamp = beijing_time.strftime('%y%m%d%H%M%S')
            self.round_id = f"{self.uid.uid:06d}{timestamp}"
        super(Round, self).save(*args, **kwargs)

    def __str__(self):
        return self.round_id
    

class Cycle(models.Model):
    # 自定义的 cycle_id，可以使用 CharField，并设置 unique=True
    cycle_id = models.CharField(max_length=60, primary_key=True, verbose_name='周期编号')

    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户编号')
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE, verbose_name='轮次编号')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    cycle_number = models.IntegerField(verbose_name='周期数字')
    has_decided = models.BooleanField(default=False, verbose_name='是否已决策')

    def save(self, *args, **kwargs):
        if not self.cycle_id:
            # 定义北京时间时区
            beijing_tz = ZoneInfo('Asia/Shanghai')
            # 将 start_time 转换为北京时间
            beijing_time = self.start_time.astimezone(beijing_tz)
            # 生成北京时间的时间戳
            timestamp = beijing_time.strftime('%y%m%d%H%M%S')
            self.cycle_id = f"{self.uid.uid:06d}{timestamp}{self.cycle_number}"
        super(Cycle, self).save(*args, **kwargs)

    def __str__(self):
        return self.cycle_id


class MarketReport(models.Model):
    # 自增报告编号，主键
    market_report_id = models.AutoField(primary_key=True, verbose_name='报告编号')
    # 本报告所属周期编号，外键
    cycle_id = models.ForeignKey('Cycle', on_delete=models.CASCADE, verbose_name='周期编号')
    # 市场容量
    market_capacity = models.CharField(max_length=255,verbose_name='市场容量')
    # 原材料
    raw_materials = models.CharField(max_length=255, verbose_name='原材料')
    # 附件
    attachments = models.CharField(max_length=255, verbose_name='附件')
    # 人员费用
    personnel_costs = models.CharField(max_length=255, verbose_name='人员费用')
    # 批量招标
    bulk_tendering = models.CharField(max_length=255, verbose_name='批量招标')
    # 批量订购
    bulk_ordering = models.CharField(max_length=255, verbose_name='批量订购')
    # 订购价格
    ordering_price = models.CharField(max_length=255,verbose_name='订购价格')

    def __str__(self):
        return f"{self.market_report_id}"
    
class MarketHistoryReport(models.Model):
    # 自增历史报告编号，主键
    history_id = models.AutoField(primary_key=True, verbose_name='历史报告编号')
    
    # 本历史报告所属周期编号，外键
    cycle_id = models.ForeignKey('Cycle', on_delete=models.CASCADE, verbose_name='周期编号')
    
    # 市场容量分段数据
    zero_to_25000_mater = models.CharField(max_length=255, verbose_name='0-25000原材料')
    zero_to_25000_att = models.CharField(max_length=255, verbose_name='0-25000附件')
    
    two_fifty_one_to_45000_mater = models.CharField(max_length=255, verbose_name='25001-45000原材料')
    two_fifty_one_to_45000_att = models.CharField(max_length=255, verbose_name='25001-45000附件')
    
    four_fifty_one_to_70000_mater = models.CharField(max_length=255, verbose_name='45001-70000原材料')
    four_fifty_one_to_70000_att = models.CharField(max_length=255, verbose_name='45001-70000附件')
    
    seven_zero_zero_one_mater = models.CharField(max_length=255, verbose_name='70001及以上原材料')
    seven_zero_zero_one_att = models.CharField(max_length=255, verbose_name='70001及以上附件')
    
    # 各项费用
    management = models.CharField(max_length=255, verbose_name='管理费用')
    sales = models.CharField(max_length=255, verbose_name='销售费用')
    purchase = models.CharField(max_length=255, verbose_name='采购费用')
    prd = models.CharField(max_length=255, verbose_name='生产费用')
    rnd = models.CharField(max_length=255, verbose_name='研发费用')
    register = models.CharField(max_length=255, verbose_name='注册费用')
    reserve = models.CharField(max_length=255, verbose_name='储备费用')
    loan = models.CharField(max_length=255, verbose_name='贷款费用')
    total = models.CharField(max_length=255, verbose_name='总费用')
    
    def __str__(self):
        return f"历史报告 {self.history_id} - 周期 {self.cycle_id}"
    

class CompetitionResult(models.Model):
    # 自增竞争表编号，主键
    competition_id = models.AutoField(primary_key=True, verbose_name='竞争表编号')
    
    # 本竞争表所属周期，外键
    cycle_id = models.ForeignKey('Cycle', on_delete=models.CASCADE, verbose_name='周期编号')
    # 竞争表标题
    competition_title = models.CharField(max_length=255, verbose_name='竞争表标题', null=True, blank=True)
    # 竞争相关字段（本企业和计算机各一）
    # 一般市场价格
    company_market_price = models.CharField(max_length=255, verbose_name='本企业一般市场价格')
    competitor_market_price = models.CharField(max_length=255, verbose_name='计算机一般市场价格')
    
    # 广告费用投入
    company_ad_expenses = models.CharField(max_length=255, verbose_name='本企业广告费用投入')
    competitor_ad_expenses = models.CharField(max_length=255, verbose_name='计算机广告费用投入')
    
    # 销售人员数量
    company_sales_staff = models.CharField(max_length=255, verbose_name='本企业销售人员数量')
    competitor_sales_staff = models.CharField(max_length=255, verbose_name='计算机销售人员数量')
    
    # 产品质量评价
    company_quality_rating = models.CharField(max_length=255, verbose_name='本企业产品质量评价')
    competitor_quality_rating = models.CharField(max_length=255, verbose_name='计算机产品质量评价')
    
    # 一般市场销售量
    company_market_sales_volume = models.CharField(max_length=255, verbose_name='本企业一般市场销售量')
    competitor_market_sales_volume = models.CharField(max_length=255, verbose_name='计算机一般市场销售量')
    
    # 一般市场销售额
    company_market_sales_revenue = models.CharField(max_length=255, verbose_name='本企业一般市场销售额')
    competitor_market_sales_revenue = models.CharField(max_length=255, verbose_name='计算机一般市场销售额')
    
    # 理论市场占有率
    company_theoretical_share = models.CharField(max_length=255, verbose_name='本企业理论市场占有率')
    competitor_theoretical_share = models.CharField(max_length=255, verbose_name='计算机理论市场占有率')
    
    # 实际市场占有率
    company_actual_share = models.CharField(max_length=255, verbose_name='本企业实际市场占有率')
    competitor_actual_share = models.CharField(max_length=255, verbose_name='计算机实际市场占有率')
    
    # 附加市场Ⅰ销售量
    company_extra1_sales_volume = models.CharField(max_length=255, verbose_name='本企业附加市场Ⅰ销售量')
    competitor_extra1_sales_volume = models.CharField(max_length=255, verbose_name='计算机附加市场Ⅰ销售量')
    
    # 附加市场Ⅰ销售额
    company_extra1_sales_revenue = models.CharField(max_length=255, verbose_name='本企业附加市场Ⅰ销售额')
    competitor_extra1_sales_revenue = models.CharField(max_length=255, verbose_name='计算机附加市场Ⅰ销售额')
    
    # 附加市场Ⅱ销售量
    company_extra2_sales_volume = models.CharField(max_length=255, verbose_name='本企业附加市场Ⅱ销售量')
    competitor_extra2_sales_volume = models.CharField(max_length=255, verbose_name='计算机附加市场Ⅱ销售量')
    
    # 附加市场Ⅱ销售额
    company_extra2_sales_revenue = models.CharField(max_length=255, verbose_name='本企业附加市场Ⅱ销售额')
    competitor_extra2_sales_revenue = models.CharField(max_length=255, verbose_name='计算机附加市场Ⅱ销售额')
    
    # 中标企业
    company_winning_company = models.CharField(max_length=255, verbose_name='本企业中标企业')
    competitor_winning_company = models.CharField(max_length=255, verbose_name='计算机中标企业')
    
    # 中标企业投标价格
    company_bid_price = models.CharField(max_length=255, verbose_name='本企业中标企业投标价格')
    competitor_bid_price = models.CharField(max_length=255, verbose_name='计算机中标企业投标价格')
    
    # 产品累积库存数量
    company_inventory = models.CharField(max_length=255, verbose_name='本企业产品累积库存数量')
    competitor_inventory = models.CharField(max_length=255, verbose_name='计算机产品累积库存数量')
    
    # 生产线生产能力
    company_capacity = models.CharField(max_length=255, verbose_name='本企业生产线生产能力')
    competitor_capacity = models.CharField(max_length=255, verbose_name='计算机生产线生产能力')
    
    # 税前经营成果
    company_profit = models.CharField(max_length=255, verbose_name='本企业税前经营成果')
    competitor_profit = models.CharField(max_length=255, verbose_name='计算机税前经营成果')
    
    # 资产负债总和
    company_assets_liabilities = models.CharField(max_length=255, verbose_name='本企业资产负债总和')
    competitor_assets_liabilities = models.CharField(max_length=255, verbose_name='计算机资产负债总和')
    
    def __str__(self):
        return f"竞争结果 {self.competition_id} - 周期 {self.cycle_id}"
    




#6
class Evaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True)  # 评价表自增编号
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)  # 当前决策轮次编号，外键
    project = models.CharField(max_length=255)  # 项目（如市场价格、广告费用等）
    company = models.CharField(max_length=255)  # 企业（计算机/本企业）
    cycle_number = models.IntegerField()  # 周期
    weight= models.FloatField(null=True, blank=True) # 权数
    value = models.FloatField()  # 值
    score_ranking = models.FloatField()  # 评分/排名
    
    def __str__(self):
        return f"Evaluation {self.evaluation_id} - Round {self.round_id} - Project {self.project}"

    class Meta:
        db_table = 'evaluation'  # 指定数据库表名
        verbose_name = 'Evaluation'  # 单数名
        verbose_name_plural = 'Evaluations'  # 复数名
