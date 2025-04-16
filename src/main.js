import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import ECharts from 'vue-echarts';
import 'echarts';

const app = createApp(App);

// 注册Element-Plus的所有图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 注册 Vue ECharts 组件
app.component('ECharts', ECharts);

app.use(router);
app.use(createPinia());
app.use(ElementPlus);
app.mount('#app');

