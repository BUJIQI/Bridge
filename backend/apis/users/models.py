from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo 
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)  # 自增用户编号
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')  # 学号
    name = models.CharField(max_length=50, verbose_name='学生姓名')  # 学生姓名
    user_class = models.CharField(max_length=50, verbose_name='班级')  # 班级
    team_name = models.CharField(max_length=50, verbose_name='队名')  # 队名
    phone = models.CharField(max_length=15, verbose_name='电话')  # 电话
    group = models.IntegerField(verbose_name='组号',null=True)  # 组号
    number = models.IntegerField(verbose_name='企业编号',null=True)  # 企业编号
    register_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间',null=True)  # 注册时间
    rest_rounds = models.IntegerField(null=True,blank=True,verbose_name='剩余重开机会')  # 剩余重开机会
    unenctypted_password = models.CharField(max_length=128, verbose_name='不被加密的密码')  # 不被加密的密码，用于重新登陆

    class Meta:
        db_table = 'my_custom_user'  
        verbose_name = "用户"
        verbose_name_plural = "用户"

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
    @classmethod
    def update_and_insert_round(cls, round_reports, user_reports):
        """
        更新现有的 round 实例，并插入一条新的 round 数据。
        """
        # 1. 更新现有的 round 实例
        round_reports.end_time = timezone.now()  # 获取当前时间
        round_reports.save()  # 保存更新

        # 2. 插入一条新的 round 数据
        new_round = cls(
            uid=user_reports,  # 外键为用户实例
        )
        new_round.save()  # 保存新实例

        return new_round  # 返回新插入的 round 实例
    

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
    
    @classmethod
    def update_and_insert_cycle(cls, cycle_reports, user_reports, round_reports, cycle_num):
        """
        更新现有的 Cycle 实例，并插入一条新的 Cycle 数据。
        """
        # 1. 更新现有的 Cycle 实例
        cycle_reports.has_decided = True
        cycle_reports.end_time = timezone.now()  # 获取当前时间
        cycle_reports.save()  # 保存更新

        if cycle_reports.cycle_number < 7:  #第七周期不需要新建周期
            # 2. 插入一条新的 Cycle 数据
            new_cycle = cls(
                uid=user_reports,  # 外键为用户实例
                round_id=round_reports,  # 外键为轮次实例
                cycle_number=cycle_num  # 新的周期编号
            )
            new_cycle.save()  # 保存新实例
            return new_cycle  # 返回新插入的 Cycle 实例
        else:
            return cycle_reports  # 返回原有的 Cycle 实例

#1.1
#1.1
#1.1
#1.1
#1.1
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

#1.2   
#1.2
#1.2
#1.2
#1.2

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
    

#2
#2
#2
#2
#2
class DecisionForm(models.Model):
    # 自增决策表单编号，主键
    decision_id = models.AutoField(primary_key=True, verbose_name='决策表单编号')
    
    # 本决策表单所属周期编号，外键
    cycle_id = models.ForeignKey('Cycle', on_delete=models.CASCADE, verbose_name='周期编号')
 
    # 本决策表单提交时间
    post_time = models.DateTimeField(default=timezone.now, verbose_name='提交时间')
    
    # 使用字符串来表示其余字段
    market_price = models.CharField(max_length=255, verbose_name='市场价格')
    ad_expense = models.CharField(max_length=255, verbose_name='广告费用投入')
    sales_count = models.CharField(max_length=255, verbose_name='销售人员个数')
    research_report = models.CharField(max_length=255, verbose_name='市场和生产研究报告')
    bid_price = models.CharField(max_length=255, verbose_name='投标价格')
    special_products_count = models.CharField(max_length=255, verbose_name='特殊产品数')
    raw_materials_qty = models.CharField(max_length=255, verbose_name='购买原材料量')
    attachments_qty = models.CharField(max_length=255, verbose_name='购买附件量')
    research_personnel_recruited = models.CharField(max_length=255, verbose_name='科研人员招收数')
    research_personnel_terminated = models.CharField(max_length=255, verbose_name='科研人员辞退数')
    improvement_cost = models.CharField(max_length=255, verbose_name='产品改进费用')
    market_plan_qty = models.CharField(max_length=255, verbose_name='一般市场产品计划量')
    production_line_investment = models.CharField(max_length=255, verbose_name='生产线投资数')
    production_line_sales = models.CharField(max_length=255, verbose_name='生产线变卖数')
    maintenance_cost = models.CharField(max_length=255, verbose_name='维修保养费用')
    production_investment = models.CharField(max_length=255, verbose_name='生产合理化投资')
    production_personnel_recruited = models.CharField(max_length=255, verbose_name='生产人员招收数')
    production_personnel_terminated = models.CharField(max_length=255, verbose_name='生产人员辞退数')
    robots_purchased = models.CharField(max_length=255, verbose_name='购买机器人')
    welfare_expense = models.CharField(max_length=255, verbose_name='社会福利费用')
    medium_loan = models.CharField(max_length=255, verbose_name='中期贷款')
    securities_purchase = models.CharField(max_length=255, verbose_name='购买有价证券')
    dividend_payment = models.CharField(max_length=255, verbose_name='计划支付股息')
    management_investment = models.CharField(max_length=255, verbose_name='管理合理化投资')

    def __str__(self):
        return f"决策表单 {self.decision_id} - 周期 {self.cycle_id}"


#4
#4
#4
#4
#4
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
#6
#6
#6
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

#用于保持爬取数据的结构
class Datakeep(models.Model):
    datakeep_id = models.AutoField(primary_key=True)  # 数据保留表自增编号
    uid = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户编号，外键
    response_look1 = models.JSONField(blank=True, null=True)  # 数据1_1
    response_lookhistory = models.JSONField(blank=True, null=True)  # 数据1_2
    response_historical_decision = models.JSONField(blank=True, null=True)  # 数据2
    compete_outcome = models.JSONField(blank=True, null=True)  # 数据4
    response_enterreporting = models.JSONField(blank=True, null=True)  # 数据5
    summart_evaluation= models.JSONField(blank=True, null=True)  # 数据6
    def __str__(self):
        return f"Datakeep {self.datakeep_id} - User {self.uid} "

    class Meta:
        db_table = 'datakeep'  # 指定数据库表名
        verbose_name = 'Datakeep'  # 单数名
        verbose_name_plural = 'Datakeeps'  # 复数名

    @classmethod
    def get_or_update_data(cls, uid, response_look1=None, response_lookhistory=None, response_historical_decision=None,
                           compete_outcome=None, response_enterreporting=None, summart_evaluation=None):
        """
        检查是否已有该uid的数据，如果没有则插入，如果有则更新数据。
        """
        # 尝试获取已有数据
        instance = cls.objects.filter(uid=uid).first()

        if instance:
            # 如果存在，则更新数据
            instance.response_look1 = response_look1 if response_look1 is not None else instance.response_look1
            instance.response_lookhistory = response_lookhistory if response_lookhistory is not None else instance.response_lookhistory
            instance.response_historical_decision = response_historical_decision if response_historical_decision is not None else instance.response_historical_decision
            instance.compete_outcome = compete_outcome if compete_outcome is not None else instance.compete_outcome
            instance.response_enterreporting = response_enterreporting if response_enterreporting is not None else instance.response_enterreporting
            instance.summart_evaluation = summart_evaluation if summart_evaluation is not None else instance.summart_evaluation
            instance.save()  # 更新数据
            return  'updated'
        else:
            # 如果没有找到，则插入新数据
            user_instance = User.objects.get(uid=uid) 
            instance = cls.objects.create(
                uid=user_instance,
                response_look1=response_look1,
                response_lookhistory=response_lookhistory,
                response_historical_decision=response_historical_decision,
                compete_outcome=compete_outcome,
                response_enterreporting=response_enterreporting,
                summart_evaluation=summart_evaluation,
            )
            return  'created'
        
    @classmethod
    def get_field_data(cls, uid, field_name):
        """
        根据 uid 和字段名返回对应字段的数据。
        """
        # 查找指定uid的Datakeep实例
        instance = cls.objects.filter(uid=uid).first()

        if instance:
            # 动态获取字段名的数据
            if hasattr(instance, field_name):
                return getattr(instance, field_name)
            else:
                return None  # 如果该字段不存在，返回 None
        else:
            return None  # 如果没有找到该uid的记录，返回None
        


#5
#5
#5
#5
#5


class CompanyReportMarket(models.Model):
    market_id = models.AutoField(primary_key=True, verbose_name='市场报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    general_price = models.CharField(max_length=255, verbose_name='一般市场价格')
    att_1_price = models.CharField(max_length=255, verbose_name='附加市场1价格')
    att_2_price = models.CharField(max_length=255, verbose_name='附加市场2价格')
    general_sales_volume = models.CharField(max_length=255, verbose_name='一般市场销售量')
    att_1_sales_volume = models.CharField(max_length=255, verbose_name='附加市场1销售量')
    att_2_sales_volume = models.CharField(max_length=255, verbose_name='附加市场2销售量')
    general_sales_revenue = models.CharField(max_length=255, verbose_name='一般市场销售额')
    att_1_sales_revenue = models.CharField(max_length=255, verbose_name='附加市场1销售额')
    att_2_sales_revenue = models.CharField(max_length=255, verbose_name='附加市场2销售额')
    share = models.CharField(max_length=255, verbose_name='市场占有率%')
    rate = models.CharField(max_length=255, verbose_name='产品质量评价')

    def __str__(self):
        return f"市场报告 {self.market_id} - 周期 {self.cycle_id}"


class CompanyReportWarehouse1(models.Model):
    warehouse_1_id = models.AutoField(primary_key=True, verbose_name='仓库报告1:原材料 编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    beginning_inventory_qty = models.CharField(max_length=255, verbose_name='期初库存量')
    beginning_inventory_value = models.CharField(max_length=255, verbose_name='期初库存价值')
    beginning_inventory_total = models.CharField(max_length=255, verbose_name='期初库存总价值')
    increase_qty = models.CharField(max_length=255, verbose_name='增加量')
    increase_value = models.CharField(max_length=255, verbose_name='增加值')
    increase_total = models.CharField(max_length=255, verbose_name='增加总值')
    consumed_qty = models.CharField(max_length=255, verbose_name='消耗量')
    consumed_value = models.CharField(max_length=255, verbose_name='消耗值')
    consumed_total = models.CharField(max_length=255, verbose_name='消耗总值')
    final_inventory_qty = models.CharField(max_length=255, verbose_name='期末库存量')
    final_inventory_value = models.CharField(max_length=255, verbose_name='期末库存价值')
    final_inventory_total = models.CharField(max_length=255, verbose_name='期末库存总值')

    def __str__(self):
        return f"仓库报告1:原材料 {self.warehouse_1_id} - 周期 {self.cycle_id}"





class CompanyReportWarehouse2(models.Model):
    warehouse_2_id = models.AutoField(primary_key=True, verbose_name='仓库报告2:一般产品 编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    beginning_inventory_qty = models.CharField(max_length=255, verbose_name='期初库存量')
    beginning_inventory_cost = models.CharField(max_length=255, verbose_name='期初制造成本')
    beginning_inventory_value = models.CharField(max_length=255, verbose_name='期初库存价值')
    increase_qty = models.CharField(max_length=255, verbose_name='增加量')
    increase_cost = models.CharField(max_length=255, verbose_name='增加成本')
    increase_value = models.CharField(max_length=255, verbose_name='增加值')
    consumed_qty = models.CharField(max_length=255, verbose_name='消耗量')
    consumed_cost = models.CharField(max_length=255, verbose_name='消耗成本')
    consumed_value = models.CharField(max_length=255, verbose_name='消耗值')
    final_inventory_qty = models.CharField(max_length=255, verbose_name='期末库存量')
    final_inventory_cost = models.CharField(max_length=255, verbose_name='期末库存成本')
    final_inventory_value = models.CharField(max_length=255, verbose_name='期末库存价值')

    def __str__(self):
        return f"仓库报告2:一般产品 {self.warehouse_2_id} - 周期 {self.cycle_id}"


class CompanyReportWarehouse3(models.Model):
    warehouse_3_id = models.AutoField(primary_key=True, verbose_name='仓库报告3:附件 编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    beginning_inventory_qty = models.CharField(max_length=255, verbose_name='期初库存量')
    beginning_inventory_value = models.CharField(max_length=255, verbose_name='期初库存价值')
    beginning_inventory_total = models.CharField(max_length=255, verbose_name='期初库存总价值')
    increase_qty = models.CharField(max_length=255, verbose_name='增加量')
    increase_value = models.CharField(max_length=255, verbose_name='增加值')
    increase_total = models.CharField(max_length=255, verbose_name='增加总值')
    consumed_qty = models.CharField(max_length=255, verbose_name='消耗量')
    consumed_value = models.CharField(max_length=255, verbose_name='消耗值')
    consumed_total = models.CharField(max_length=255, verbose_name='消耗总值')
    final_inventory_qty = models.CharField(max_length=255, verbose_name='期末库存量')
    final_inventory_value = models.CharField(max_length=255, verbose_name='期末库存价值')
    final_inventory_total = models.CharField(max_length=255, verbose_name='期末库存总值')

    def __str__(self):
        return f"仓库报告3:附件 {self.warehouse_3_id} - 周期 {self.cycle_id}"


class CompanyReportPersonnel1(models.Model):
    personnel_1_id = models.AutoField(primary_key=True, verbose_name='人员报告1编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    beginning_personnel_prd = models.CharField(max_length=255, verbose_name='生产部门期初人员')
    beginning_personnel_rnd = models.CharField(max_length=255, verbose_name='研究开发部门期初人员')
    recruitment_prd = models.CharField(max_length=255, verbose_name='生产部门招聘人数')
    recruitment_rnd = models.CharField(max_length=255, verbose_name='研究开发部门招聘人数')
    fire_prd = models.CharField(max_length=255, verbose_name='生产部门辞退人数')
    fire_rnd = models.CharField(max_length=255, verbose_name='研究开发部门辞退人数')
    flow_prd = models.CharField(max_length=255, verbose_name='生产部门流动人数')
    flow_rnd = models.CharField(max_length=255, verbose_name='研究开发部门流动人数')
    final_personnel_prd = models.CharField(max_length=255, verbose_name='生产部门期末人员')
    final_personnel_rnd = models.CharField(max_length=255, verbose_name='研究开发部门期末人员')

    def __str__(self):
        return f"人员报告1 {self.personnel_1_id} - 周期 {self.cycle_id}"


class CompanyReportPersonnel2(models.Model):
    personnel_2_id = models.AutoField(primary_key=True, verbose_name='人员报告2编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    sales = models.CharField(max_length=255, verbose_name='销售部门人员数')
    purchase = models.CharField(max_length=255, verbose_name='采购部门人员数')
    management = models.CharField(max_length=255, verbose_name='管理部门人员数')
    coefficient = models.CharField(max_length=255, verbose_name='管理的合理化系数')

    def __str__(self):
        return f"人员报告2 {self.personnel_2_id} - 周期 {self.cycle_id}"


class CompanyReportPrd1(models.Model):
    prd_1_id = models.AutoField(primary_key=True, verbose_name='生产报告1编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    prev_line = models.CharField(max_length=255, verbose_name='前周期生产线')
    prev_robot = models.CharField(max_length=255, verbose_name='前周期机器人')
    invest_line = models.CharField(max_length=255, verbose_name='投资生产线')
    invest_robot = models.CharField(max_length=255, verbose_name='投资机器人')
    sell_line = models.CharField(max_length=255, verbose_name='变卖生产线')
    sell_robot = models.CharField(max_length=255, verbose_name='变卖机器人')
    curr_line = models.CharField(max_length=255, verbose_name='本周期生产线')
    curr_robot = models.CharField(max_length=255, verbose_name='本周期机器人')

    def __str__(self):
        return f"生产报告1 {self.prd_1_id} - 周期 {self.cycle_id}"


class CompanyReportPrd2(models.Model):
    prd_2_id = models.AutoField(primary_key=True, verbose_name='生产报告2编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    general_process = models.CharField(max_length=255, verbose_name='一般产品加工台数')
    general_facility = models.CharField(max_length=255, verbose_name='一般产品设备要求数')
    general_personnel = models.CharField(max_length=255, verbose_name='一般产品人员要求数')
    sp_process = models.CharField(max_length=255, verbose_name='特殊产品加工台数')
    sp_facility = models.CharField(max_length=255, verbose_name='特殊产品设备要求数')
    sp_personnel = models.CharField(max_length=255, verbose_name='特殊产品人员要求数')
    total_process = models.CharField(max_length=255, verbose_name='总产品加工台数')
    total_facility = models.CharField(max_length=255, verbose_name='总产品设备要求数')
    total_personnel = models.CharField(max_length=255, verbose_name='总产品人员要求数')
    load_process = models.CharField(max_length=255, verbose_name='加工台数负载率%')
    load_facility = models.CharField(max_length=255, verbose_name='设备要求数负载率%')
    load_personnel = models.CharField(max_length=255, verbose_name='人员要求数负载率%')

    def __str__(self):
        return f"生产报告2 {self.prd_2_id} - 周期 {self.cycle_id}"


class CompanyReportPrd3(models.Model):
    prd_3_id = models.AutoField(primary_key=True, verbose_name='生产报告3编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    rational = models.CharField(max_length=255, verbose_name='生产线合理化系数')
    maintain = models.CharField(max_length=255, verbose_name='生产线维修保养系数')
    load_100 = models.CharField(max_length=255, verbose_name='生产线负载率100%时生产能力')

    def __str__(self):
        return f"生产报告3 {self.prd_3_id} - 周期 {self.cycle_id}"

class CompanyReportCostType(models.Model):
    cost_t_id = models.AutoField(primary_key=True, verbose_name='成本类型核算报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    raw_material = models.CharField(max_length=255, verbose_name='原材料')
    attachment = models.CharField(max_length=255, verbose_name='附件')
    prd_material = models.CharField(max_length=255, verbose_name='生产材料')
    salary = models.CharField(max_length=255, verbose_name='工资费用')
    salary_direct = models.CharField(max_length=255, verbose_name='直接工资费用')
    personnel = models.CharField(max_length=255, verbose_name='人员附加费用')
    personnel_direct = models.CharField(max_length=255, verbose_name='直接人员附加费用')
    hirefire = models.CharField(max_length=255, verbose_name='招聘/解雇费用')
    plant = models.CharField(max_length=255, verbose_name='厂房')
    line = models.CharField(max_length=255, verbose_name='生产线')
    robot = models.CharField(max_length=255, verbose_name='机器人')
    other_fixed = models.CharField(max_length=255, verbose_name='其他固定费用')
    maintain = models.CharField(max_length=255, verbose_name='维修费用')
    rationalization = models.CharField(max_length=255, verbose_name='合理化')
    repair = models.CharField(max_length=255, verbose_name='返修/废品')
    inventory = models.CharField(max_length=255, verbose_name='库存费用')
    ad = models.CharField(max_length=255, verbose_name='广告费用')
    market_research = models.CharField(max_length=255, verbose_name='市场研究')
    other_rnd = models.CharField(max_length=255, verbose_name='其它研究开发费用')
    total = models.CharField(max_length=255, verbose_name='总费用')

    def __str__(self):
        return f"产品成本类型核算报告 {self.cost_t_id} - 周期 {self.cycle_id}"




class CompanyReportCostDpt(models.Model):
    cost_d_id = models.AutoField(primary_key=True, verbose_name='成本部门核算报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    cost_dpt = models.CharField(max_length=255, verbose_name='成本发生部门名称')
    total = models.CharField(max_length=255, verbose_name='合计')
    purchase = models.CharField(max_length=255, verbose_name='采购成本')
    prd = models.CharField(max_length=255, verbose_name='生产成本')
    rnd = models.CharField(max_length=255, verbose_name='研发成本')
    inventory = models.CharField(max_length=255, verbose_name='销售库存成本')
    management = models.CharField(max_length=255, verbose_name='管理成本')

    def __str__(self):
        return f"成本发生部门核算报告 {self.cost_d_id} - 周期 {self.cycle_id}"





class CompanyReportCostUnit(models.Model):
    cost_u_id = models.AutoField(primary_key=True, verbose_name='成本承担单元核算报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    cost_unit = models.CharField(max_length=255, verbose_name='成本承担单元名称')
    general_market = models.CharField(max_length=255, verbose_name='一般市场')
    attach_market_1 = models.CharField(max_length=255, verbose_name='附加市场Ⅰ')
    attach_market_2 = models.CharField(max_length=255, verbose_name='附加市场Ⅱ')
    total = models.CharField(max_length=255, verbose_name='总成本')

    def __str__(self):
        return f"成本承担单元核算报告 {self.cost_u_id} - 周期 {self.cycle_id}"


class CompanyReportProfitLoss(models.Model):
    pro_los_id = models.AutoField(primary_key=True, verbose_name='利润与亏损报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    revenue = models.CharField(max_length=255, verbose_name='销售收入')

    inventory_change = models.CharField(max_length=255, verbose_name='产品库存变化')
    production = models.CharField(max_length=255, verbose_name='销售产品制造成本')
    material = models.CharField(max_length=255, verbose_name='材料费用')
    sales = models.CharField(max_length=255, verbose_name='销售费用')
    salary = models.CharField(max_length=255, verbose_name='工资')
    personnel_att = models.CharField(max_length=255, verbose_name='人员附加费用')
    r_and_d = models.CharField(max_length=255, verbose_name='研究开发费用')
    other_personnel = models.CharField(max_length=255, verbose_name='其他人员费用')
    depreciation = models.CharField(max_length=255, verbose_name='折旧')
    management = models.CharField(max_length=255, verbose_name='管理费用')
    other_operating = models.CharField(max_length=255, verbose_name='其他经营费用')
    operating_profit = models.CharField(max_length=255, verbose_name='生产经营成果')

    def __str__(self):
        return f"利润和亏损核算报告 {self.pro_los_id} - 周期 {self.cycle_id}"


class CompanyReportPostTaxProfit(models.Model):
    post_tax_id = models.AutoField(primary_key=True, verbose_name='税后利润报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    operating_profit = models.CharField(max_length=255, verbose_name='生产经营成果')
    securities_income = models.CharField(max_length=255, verbose_name='有价证券收入')
    interest = models.CharField(max_length=255, verbose_name='利息费用和其他费用')
    general_profit = models.CharField(max_length=255, verbose_name='一般经营成果')
    sp_income = models.CharField(max_length=255, verbose_name='特别收入')
    sp_expense = models.CharField(max_length=255, verbose_name='特别费用')
    pre_tax_profit = models.CharField(max_length=255, verbose_name='特别费用')
    tax = models.CharField(max_length=255, verbose_name='税收')
    netprofit = models.CharField(max_length=255, verbose_name='周期结余/周期亏损')

    def __str__(self):
        return f"税后利润核算报告 {self.post_tax_id} - 周期 {self.cycle_id}"


class CompanyReportProfitDistribution(models.Model):
    distribution_id = models.AutoField(primary_key=True, verbose_name='利润分配报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    period_profit = models.CharField(max_length=255, verbose_name='周期结余/周期亏损')
    previous_loss = models.CharField(max_length=255, verbose_name='前周期亏损结转')
    current_profit = models.CharField(max_length=255, verbose_name='本周期利润储备')
    capital_balance_profit = models.CharField(max_length=255, verbose_name='资金平衡利润/资金平衡亏损')
    dividend = models.CharField(max_length=255, verbose_name='股息')
    final_loss = models.CharField(max_length=255, verbose_name='本周期亏损结转')

    def __str__(self):
        return f"利润分配核算报告 {self.distribution_id} - 周期 {self.cycle_id}"


class CompanyReportFinancial(models.Model):
    financial_id = models.AutoField(primary_key=True, verbose_name='财务报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    beginning_cash = models.CharField(max_length=255, verbose_name='期初现金')
    current_sales = models.CharField(max_length=255, verbose_name='本周期产品销售收入')
    material = models.CharField(max_length=255, verbose_name='材料费用')
    previous_sales = models.CharField(max_length=255, verbose_name='前周期产品销售收入')
    labor = models.CharField(max_length=255, verbose_name='人员费用')
    other_operating = models.CharField(max_length=255, verbose_name='其他经营费用')
    security_income = models.CharField(max_length=255, verbose_name='有价证券 ')
    loan_repay = models.CharField(max_length=255, verbose_name='中期和透支贷款归还')
    interest_income = models.CharField(max_length=255, verbose_name='利息收入')
    interest_expense = models.CharField(max_length=255, verbose_name='利息费用')
    robots = models.CharField(max_length=255, verbose_name='购买机器人')
    special_income = models.CharField(max_length=255, verbose_name='特殊收入')
    line_purchase = models.CharField(max_length=255, verbose_name='购买生产线和厂房')
    line_sales = models.CharField(max_length=255, verbose_name='生产线变卖收入')
    security_sales = models.CharField(max_length=255, verbose_name='购买有价证券')
    tax = models.CharField(max_length=255, verbose_name='税收')
    mid_loan = models.CharField(max_length=255, verbose_name='中期贷款')
    dividend = models.CharField(max_length=255, verbose_name=' 股息支付(前周期)')
    overdraft_loan = models.CharField(max_length=255, verbose_name='透支贷款')
    special_expense = models.CharField(max_length=255, verbose_name='特别费用')
    total_income = models.CharField(max_length=255, verbose_name='现金收入合计') 
    total_expense = models.CharField(max_length=255, verbose_name='现金支出合计')
    ending_cash = models.CharField(max_length=255, verbose_name='期末现金')

    def __str__(self):
        return f"生产经营财务报告 {self.financial_id} - 周期 {self.cycle_id}"


class CompanyReportBalance(models.Model):
    balance_id = models.AutoField(primary_key=True, verbose_name='资产负债表编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    registered_capital = models.CharField(max_length=255, verbose_name='注册资金')
    estate = models.CharField(max_length=255, verbose_name='地产和厂房')
    capital_reserves = models.CharField(max_length=255, verbose_name='资金储备')
    facility = models.CharField(max_length=255, verbose_name='设备和生产设施')
    retained_earnings = models.CharField(max_length=255, verbose_name='利润储备')
    previous_loss = models.CharField(max_length=255, verbose_name='前周期亏损结转')
    current_trans = models.CharField(max_length=255, verbose_name='周期结余/周期亏损')
    material_att = models.CharField(max_length=255, verbose_name='原材料与附件')
    finished_product = models.CharField(max_length=255, verbose_name='成品')
    accounts_receivable = models.CharField(max_length=255, verbose_name='债权')
    long_loan = models.CharField(max_length=255, verbose_name='长期贷款')
    security = models.CharField(max_length=255, verbose_name='有价证券')
    mid_loan = models.CharField(max_length=255, verbose_name='中期贷款')
    cash = models.CharField(max_length=255, verbose_name='现金')
    short_loan = models.CharField(max_length=255, verbose_name='透支贷款')
    total_assets = models.CharField(max_length=255, verbose_name='资产合计')
    total_liabilities = models.CharField(max_length=255, verbose_name='负债合计')

    def __str__(self):
        return f"资产负债合计报告 {self.balance_id} - 周期 {self.cycle_id}"


class CompanyReportMarketPrd(models.Model):
    market_prd_id = models.AutoField(primary_key=True, verbose_name='各企业市场营销及生产研究报告编号')
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE, verbose_name='周期编号')
    company_compute = models.CharField(max_length=255, verbose_name='企业/计算机')
    market_price = models.CharField(max_length=255, verbose_name='一般市场价格')
    ad_expenses = models.CharField(max_length=255, verbose_name='广告费用投入')
    num_staff = models.CharField(max_length=255, verbose_name='销售人员数量')
    sales_staff = models.CharField(max_length=255, verbose_name='销售人员费用')
    product_rating = models.CharField(max_length=255, verbose_name='产品质量评价')
    product_expense = models.CharField(max_length=255, verbose_name='产品研究费用')
    market_sales_volume = models.CharField(max_length=255, verbose_name='一般市场销售量')
    market_sales_revenue = models.CharField(max_length=255, verbose_name='一般市场销售额')
    theoretical_share = models.CharField(max_length=255, verbose_name='理论市场占有率')
    actual_share = models.CharField(max_length=255, verbose_name='实际市场占有率')
    extra1_sales_volume = models.CharField(max_length=255, verbose_name='附加市场Ⅰ销售量')
    extra1_sales_revenue = models.CharField(max_length=255, verbose_name='附加市场Ⅰ销售额')
    extra2_sales_volume = models.CharField(max_length=255, verbose_name='附加市场Ⅱ销售量')
    extra2_sales_revenue = models.CharField(max_length=255, verbose_name='附加市场Ⅱ销售额')
    winning_company = models.CharField(max_length=255, verbose_name='中标企业')
    bid_price = models.CharField(max_length=255, verbose_name='中标企业投标价格')
    material_inventory = models.CharField(max_length=255, verbose_name='原材料库存量')
    attachment_inventory = models.CharField(max_length=255, verbose_name='附件库存量')
    inventory = models.CharField(max_length=255, verbose_name='产品积累库存数量')
    robots = models.CharField(max_length=255, verbose_name='机器人数量')
    researh_stuff = models.CharField(max_length=255, verbose_name='研发人员数')
    general_market_plan = models.CharField(max_length=255, verbose_name='一般市场计划量')
    general_market_prd = models.CharField(max_length=255, verbose_name='一般市场生产量')
    maintain_coe = models.CharField(max_length=255, verbose_name='维修保养系数')
    rationalization_coe = models.CharField(max_length=255, verbose_name='合理化系数')
    prd_capacity = models.CharField(max_length=255, verbose_name='生产线生产能力')
    prd_personnel = models.CharField(max_length=255, verbose_name='生产线人员数')
    prd_line_load = models.CharField(max_length=255, verbose_name='生产线负载率')
    prd_personnel_load = models.CharField(max_length=255, verbose_name='生产线人员负载率')
    general_market_cost = models.CharField(max_length=255, verbose_name='一般市场的产品成本')
    profit = models.CharField(max_length=255, verbose_name='税前经营成果')
    curr_loss = models.CharField(max_length=255, verbose_name='本周期亏损结转')
    curr_dividend = models.CharField(max_length=255, verbose_name='本周期股息支付')
    curr_profit = models.CharField(max_length=255, verbose_name='本周期利润储备')
    curr_mid = models.CharField(max_length=255, verbose_name='本周期中期贷款')
    curr_ending = models.CharField(max_length=255, verbose_name='本周期期末现金')
    total_profit = models.CharField(max_length=255, verbose_name='总的利润储备额')
    curr_loan = models.CharField(max_length=255, verbose_name='本周期透支贷款')
    assets_liabilities = models.CharField(max_length=255, verbose_name='资产负债总和')

    def __str__(self):
        return f"各企业市场营销及生产研究报告 {self.market_prd_id} - 周期 {self.cycle_id}"


#名词解释
class Term(models.Model):
    term_id=models.AutoField(primary_key=True,verbose_name='名词编号')
    term_name=models.CharField(max_length=255,verbose_name='名词')
    term_short=models.CharField(max_length=255,verbose_name='名词简介')
    term_txt1=models.TextField(verbose_name='文本一',null=True,blank=True)
    term_emph=models.CharField(max_length=255,verbose_name='强调',null=True,blank=True)
    term_list=models.TextField(max_length=255,verbose_name='列表',null=True,blank=True)
    term_equation=models.TextField(max_length=255,verbose_name='公式',null=True,blank=True)
    term_txt2=models.TextField(verbose_name='文本二',null=True,blank=True)
    term_tablename=models.CharField(max_length=255,verbose_name='表格名称',null=True,blank=True)
    term_tablehead=models.CharField(max_length=255,verbose_name='表头',null=True,blank=True)
    term_tabledata=models.CharField(max_length=255,verbose_name='表数据',null=True,blank=True)
    term_img=models.CharField(max_length=255,verbose_name='图片链接',null=True,blank=True)
    def __str__(self):
        return f"名词解释 {self.term_id} - {self.term_name}"