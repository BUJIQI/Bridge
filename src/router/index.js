import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue'; 
import UserRegister from '../components/UserRegister.vue'; 
import DecisionSimulation from '../components/DecisionSimulation.vue'; 
import ImportantInformation from '../components/ImportantInformation.vue';
import FirstPeriod from '../components/FirstPeriod.vue';
import WelcomeMessage from '../components/WelcomeMessage.vue';
import InputData from '../components/InputData.vue';
import HistoryDecision from '../components/HistoryDecision.vue';
import CompetitionOutcome from '../components/CompetitionOutcome.vue';

const routes = [
    {
        path: '/login',
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
        path: '/decision',
        name: 'Decision',
        component: DecisionSimulation,
        meta: { title: '决策仿真' }, 
        children: [
            {
                path: '/welcome',
                name: 'Welcome',
                component: WelcomeMessage,
                meta: { title: '欢迎' }
            },
            {
                path: '/market/cycle/1',
                name: 'Period1',
                component: FirstPeriod,
                meta: { title: '第1周期' }
            },  
            {
                path: '/important',
                name: 'Important',
                component: ImportantInformation,
                meta: { title: '重要信息' }
            }, 
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
                path: '/outcome',
                name: 'Outcome',  
                component: CompetitionOutcome,
                meta: { title: '竞争结果报表' }
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
