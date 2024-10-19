import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue'; 
import UserRegister from '../components/UserRegister.vue'; 
import DecisionSimulation from '../components/DecisionSimulation.vue'; 
import ImportantInformation from '../components/ImportantInformation.vue';
import FirstPeriod from '../components/FirstPeriod.vue';
import WelcomeMessage from '../components/WelcomeMessage.vue';

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
                path: '/market/cycle/一',
                name: 'Period1',
                component: FirstPeriod,
                meta: { title: '第1周期' }
            },           
        ]
    },
    {
        path: '/important',
        name: 'Important',
        component: ImportantInformation,
        meta: { title: '重要信息' }
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
