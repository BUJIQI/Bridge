import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '@/components/UserLogin.vue'; 
import UserRegister from '@/components/UserRegister.vue'; 
import DecisionSimulation from '@/components/DecisionSimulation.vue'; 
import ImportantInformation from '@/components/ImportantInformation.vue';
import PeriodSituation from '@/components/PeriodSituation.vue';
import HistoryAverage from '@/components/HistoryAverage.vue';  
import WelcomeMain from '@/components/WelcomeMain.vue';
import InputData from '@/components/InputData.vue';
import HistoryDecision from '@/components/HistoryDecision.vue';
import CompetitionOutcome from '@/components/CompetitionOutcome.vue';
import MarketProduction from '@/components/MarketProduction.vue';
import CostType from '@/components/CostType.vue';
import CostDepartment from '@/components/CostDepartment.vue';
import CostUnit from '@/components/CostUnit.vue';
import ProfitLoss from '@/components/ProfitLoss.vue';
import AfterTax from '@/components/AfterTax.vue';
import ProfitDistribution from '@/components/ProfitDistribution.vue';
import OperatingFinancial from '@/components/OperatingFinancial.vue';
import BalanceSheet from '@/components/BalanceSheet.vue';
import MarketResearch from '@/components/MarketResearch.vue';
import MarketIndex from '@/components/MarketIndex.vue';
import ProductionIndex from '@/components/ProductionIndex.vue';
import FinanceIndex from '@/components/FinanceIndex.vue';
import OverallEvaluation from '@/components/OverallEvaluation.vue';
import IndexWeight from '@/components/IndexWeight.vue';
import UserProfile from '@/components/UserProfile.vue';

const routes = [
    {
        path: '/',
        name: 'Login',
        component: UserLogin,
        meta: { title: '登录' }
    },
    {
        path: '/register',
        name: 'Register',
        component: UserRegister,
        meta: { title: '注册' }
    },
    {
        path: '/welcome',
        name: 'Welcome',
        component: WelcomeMain,
        meta: { title: '欢迎' }, 
        children: [
            {
                path: '/decision',
                name: 'Decision',
                component: DecisionSimulation,
                meta: { title: '决策仿真' },
                children: [
                    {
                        path: '/decison/input',
                        name: 'Input',
                        component: InputData,
                        meta: { title: '决策数据输入' }
                    },  
                    {
                        path: '/market/history-data/1',
                        name: 'History1',
                        component: HistoryDecision,
                        meta: { title: '第1周期历史决策' }
                    }, 
                    {
                        path: '/market/history-data/2',
                        name: 'History2',
                        component: HistoryDecision,
                        meta: { title: '第2周期历史决策' }
                    }, 
                    {
                        path: '/market/history-data/3',
                        name: 'History3',
                        component: HistoryDecision,
                        meta: { title: '第3周期历史决策' }
                    }, 
                    {
                        path: '/market/history-data/4',
                        name: 'History4',
                        component: HistoryDecision,
                        meta: { title: '第4周期历史决策' }
                    }, 
                    {
                        path: '/market/history-data/5',
                        name: 'History5',
                        component: HistoryDecision,
                        meta: { title: '第5周期历史决策' }
                    }, 
                    {
                        path: '/market/history-data/6',
                        name: 'History6',
                        component: HistoryDecision,
                        meta: { title: '第6周期历史决策' }
                    },                  
                    {
                        path: '/market/history-data/7',
                        name: 'History7',
                        component: HistoryDecision,
                        meta: { title: '第7周期历史决策' }
                    }, 
                    {
                        path: '/market/cycle/1',
                        name: 'Period1',
                        component: PeriodSituation,
                        meta: { title: '第1周期' }
                    },  
                    {
                        path: '/market/cycle/2',
                        name: 'Period2',
                        component: PeriodSituation,
                        meta: { title: '第2周期' }
                    }, 
                    {
                        path: '/market/cycle/3',
                        name: 'Period3',
                        component: PeriodSituation,
                        meta: { title: '第3周期' }
                    }, 
                    {
                        path: '/market/cycle/4',
                        name: 'Period4',
                        component: PeriodSituation,
                        meta: { title: '第4周期' }
                    }, 
                    {
                        path: '/market/cycle/5',
                        name: 'Period5',
                        component: PeriodSituation,
                        meta: { title: '第5周期' }
                    }, 
                    {
                        path: '/market/cycle/6',
                        name: 'Period6',
                        component: PeriodSituation,
                        meta: { title: '第6周期' }
                    }, 
                    {
                        path: '/market/cycle/7',
                        name: 'Period7',
                        component: PeriodSituation,
                        meta: { title: '第7周期' }
                    }, 
                    {
                        path: '/market/cycle/average',
                        name: 'Average',
                        component: HistoryAverage,
                        meta: { title: '历史平均' }
                    }, 
                    {
                        path: '/outcome',
                        name: 'Outcome',  
                        component: CompetitionOutcome,
                        meta: { title: '竞争结果报表' }
                    },
                    {
                        path: '/company/market-production',
                        name: 'Production',
                        component: MarketProduction,
                        meta: { title: '市场生产数据报告' }
                    },
                    {
                        path: '/company/cost-type',
                        name: 'CostType',
                        component: CostType,
                        meta: { title: '产品成本类型报告' }
                    },
                    {
                        path: '/company/cost-department',
                        name: 'CostDepartment',
                        component: CostDepartment,
                        meta: { title: '成本发生部门报告' }
                    },
                    {
                        path: '/company/cost-unit',
                        name: 'CostUnit',
                        component: CostUnit,
                        meta: { title: '成本承担单位报告' }
                    },
                    {
                        path: '/company/profit-loss',
                        name: 'ProfitLoss',
                        component: ProfitLoss,
                        meta: { title: '利润亏损核算报告' }
                    },
                    {
                        path: '/company/after-tax-profit',
                        name: 'AfterTax',
                        component: AfterTax,
                        meta: { title: '税后利润核算报告' }
                    },
                    {
                        path: '/company/profit-distribution',
                        name: 'ProfitDistribution',
                        component: ProfitDistribution,
                        meta: { title: '利润分配核算报告' }
                    },
                    {
                        path: '/company/operating-financial',
                        name: 'OperatingFinancial',
                        component: OperatingFinancial,
                        meta: { title: '生产经营财务报告' }
                    },
                    {
                        path: '/company/balance-sheet',
                        name: 'BalanceSheet',
                        component: BalanceSheet,
                        meta: { title: '资产负债合计报告' }
                    },
                    {
                        path: '/company/market-research',
                        name: 'MarketResearch',
                        component: MarketResearch,
                        meta: { title: '竞争市场调研报告' }
                    },
                    {
                        path: '/evaluation/market',
                        name: 'MarketIndex',
                        component: MarketIndex,
                        meta: { title: '市场类指数报告' }
                    },
                    {
                        path: '/evaluation/production',
                        name: 'ProductionIndex',
                        component: ProductionIndex,
                        meta: { title: '生产类指数报告' }
                    },
                    {
                        path: '/evaluation/finance',
                        name: 'FinanceIndex',
                        component: FinanceIndex,
                        meta: { title: '财务类指数报告' }
                    },
                    {
                        path: '/evaluation/overall',
                        name: 'OverallEvaluation',
                        component: OverallEvaluation,
                        meta: { title: '决策综合评价' }
                    },    
                    {
                        path: '/evaluation/weight',
                        name: 'IndexWeight',
                        component: IndexWeight,
                        meta: { title: '评价指标权重' }
                    },            
                ]
            },
            {
                path: '/important',
                name: 'Important',
                component: ImportantInformation,
                meta: { title: '重要信息' }
            },             
            {
                path: '/profile',
                name: 'Profile',
                component: UserProfile,
                meta: { title: '我的资料' }
            },
        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 设置页面标题的导航守卫
router.beforeEach((to, from, next) => {
    document.title = to.meta.title || '默认标题'; 
    next();
  });

export default router;
