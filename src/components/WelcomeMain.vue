<template>
  <div class="full">
    <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/welcome" @click="handleNavClick('/welcome')">
          <img src="@/assets/info.gif" alt="ICEDSS" width="40" height="40">
          JCTD
        </router-link>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/decision" @click="handleNavClick('/decision')">决策仿真</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/important" @click="handleNavClick('/important')">重要信息</router-link>
            </li>
            <li class="nav-item">
              <button @click="reset" class="btn btn-danger" style="padding: 5px; margin: 5px;">
                新的一轮
              </button>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <div class="info" style="border: 1px solid #ccc; padding: 5px; margin: 5px; border-radius: 20px;">
                当前：
                第<span class="text-danger">{{ userInfo?.group }}</span>组
                第<span class="text-danger">{{ userInfo?.number }}</span>企业
                <span class="text-danger">{{ userInfo?.rival }}</span>位竞争对手
                第<span class="text-danger">{{ userInfo?.cycle }}</span>周期
              </div>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/logout">注销</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile" @click="handleNavClick('/profile')">我的资料</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div v-if="showDefaultContent" class="row h-100">
        <div class="container">
          <h1 class="title">欢迎来到</h1>
          <h1 class="title">现代企业创业决策仿真系统</h1>
          <h2 class="subtitle">——人机对抗版</h2>
        </div>
      </div>
      <router-view v-else></router-view>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;
    const route = useRoute();

    // 从 sessionStorage 中获取 currentPath
    const currentPath = sessionStorage.getItem('currentPath') || '/welcome';
    const showDefaultContent = ref(currentPath === '/welcome');

    // 监听路由变化，并保存 currentPath 到 sessionStorage
    watch(
      () => route.path,
      (newPath) => {
        showDefaultContent.value = newPath === '/welcome';
        sessionStorage.setItem('currentPath', newPath);
      }
    );

    const handleNavClick = (path) => {
      showDefaultContent.value = path === '/welcome';
      sessionStorage.setItem('currentPath', path);
    };

    const reset = async () => {
      const confirmation = await Swal.fire({
        title: '确认重置',
        text: '您确定要重置为新的一轮吗？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      });

      if (confirmation.isConfirmed) {
        try {
          const response = await axios.get('http://127.0.0.1:8000/users/new_rounds/', { withCredentials: true });
          const data = response.data;

          if (data.restronundmum > 0) {
            // 有重开次数的情况
            Swal.fire({
              title: '成功!',
              html: `${data.state}<br>请注意剩余次数为 ${data.restronundmum} 次`,
              icon: 'success',
              confirmButtonText: '确定'
            }).then(() => {
              // 重置周期
              const userInfoString = sessionStorage.getItem('userInfo');
              const userInfoObject = JSON.parse(userInfoString);
              userInfoObject.cycle = 1;
              sessionStorage.setItem('userInfo', JSON.stringify(userInfoObject));
              // 自动刷新页面
              window.location.reload();
            });
          } else {
            // 没有重开次数的情况
            Swal.fire({
              title: '已达上限!',
              text: data.state,
              icon: 'info',
              confirmButtonText: '确定'
            });
          }
        } catch (error) {
          console.error('请求错误:', error);
          Swal.fire({
            title: '请求失败!',
            text: '请求后台失败，请稍后重试。',
            icon: 'error',
            confirmButtonText: '确定'
          });
        }
      }
    };

    return {
      userInfo,
      showDefaultContent,
      reset,
      handleNavClick,
    };
  },
};
</script>

<style scoped>
.full {
  height: 100vh;
  width: 100vw;
}

.nav-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #3c3737;
}

.nav-item {
  color: #ffffff;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 50px);
  padding: 20px;
  background: linear-gradient(to bottom right, #f0f4f8, #edd4d4);
  font-family: 'Arial', sans-serif;
  text-align: center;
}

.title {
  font-size: 50px;
  color: #333;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  margin: 10px 0;
  transition: color 0.3s;
}

.title:hover {
  color: #bd5858;
}

.subtitle {
  font-size: 24px;
  color: #666;
  margin: 5px 0;
  padding: 0 10px;
  border-left: 3px solid #bd5858;
  padding-left: 10px;
  transition: color 0.3s, transform 0.3s;
}

.subtitle:hover {
  color: #bd5858;
  transform: scale(1.05);
}
</style>
