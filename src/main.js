import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


createApp(App)
    .use(router)
    .use(createPinia())
    .mount('#app');

// 应用启动后直接跳转到登录页面
router.push('/login');
