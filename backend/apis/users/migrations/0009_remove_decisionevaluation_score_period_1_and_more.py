# Generated by Django 5.0.7 on 2024-11-27 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_productionindicator_period_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_1',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_2',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_3',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_4',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_5',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_6',
        ),
        migrations.RemoveField(
            model_name='decisionevaluation',
            name='score_period_7',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_1',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_2',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_3',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_4',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_5',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_6',
        ),
        migrations.RemoveField(
            model_name='financialindicator',
            name='period_7',
        ),
        migrations.AddField(
            model_name='decisionevaluation',
            name='overall_decision_evaluation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='经营决策综合评价'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='period_dividend_payment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='周期支付股息'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='period_end_cash',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='周期期末现金'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='period_loan_total',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='周期贷款总额'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='period_tax_payment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='周期缴纳税收'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='pre_tax_operating_result',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='税前经营成果'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='total_assets_liabilities',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='资产负债合计'),
        ),
        migrations.AddField(
            model_name='financialindicator',
            name='total_profit_loss',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='总的盈亏累计'),
        ),
    ]