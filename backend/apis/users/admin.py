from django.contrib import admin

# Register your models here.
from .models import User,Round,Cycle,MarketReport,MarketHistoryReport,CompetitionResult,Evaluation

admin.site.register(User)
admin.site.register(Round)
admin.site.register(Cycle)
admin.site.register(MarketReport)
admin.site.register(MarketHistoryReport)
admin.site.register(CompetitionResult)
admin.site.register(Evaluation)

