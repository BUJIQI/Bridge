import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue'; // 登录组件
import UserRegister from '../components/UserRegister.vue'; // 注册组件
import MainComponent from '../components/MainComponent.vue'; // 主页组件(原HelloWorld)

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
        path: '/main',
        name: 'Main',
        component: MainComponent,
        meta: { title: '主页' }
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
