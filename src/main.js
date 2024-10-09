import { createApp } from 'vue';
import App from './App.vue';
import router from './router';


createApp(App)
    .use(router)
    .mount('#app');

// 应用启动后直接跳转到登录页面
router.push('/login');
