<template>
  <div>
    <!-- 全局导航栏 -->
    <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <!-- 网页链接 -->
        <router-link class="navbar-brand" to="/" >
          <img src="@/assets/info.gif" alt="ICEDSS" width="40" height="40">
          JCTD
        </router-link>

        <!-- 触发按钮，用于小屏幕设备 -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 折叠的导航内容 -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/decision">决策仿真</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/important">重要信息</router-link>
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
                <span v-if="userInfo?.cycle !== 8">第<span class="text-danger">{{ userInfo?.cycle }}</span>周期</span>
              </div>
            </li>
            <li class="nav-item">
              <button @click="logout" class="nav-link">注销</button>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">我的资料</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>  

    <!-- 子路由内容 -->
    <div class="container-fluid">
      <router-view />
    </div>
  </div>  
</template>

<script>
import { useUserStore } from '@/store/user';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;
    const router = useRouter();
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
              const userInfoString = localStorage.getItem('userInfo');
              const userInfoObject = JSON.parse(userInfoString);
              userInfoObject.cycle = 1;
              localStorage.setItem('userInfo', JSON.stringify(userInfoObject));
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
    
    // 注销用户
    const logout = async () => {
      const confirmation = await Swal.fire({
        title: '确认注销',
        text: '您确定要注销账户吗？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      });

      if (confirmation.isConfirmed) {
        try {
          const response = await axios.get('http://127.0.0.1:8000/users/loginout/', {
            withCredentials: true 
          });

          const { status } = response;
          if (status === 200) {
            Swal.fire({
              title: '注销成功',
              icon: 'success'
            });

            localStorage.clear();
            router.push('/login');
          }
        } catch (error) {
          Swal.fire({
            title: '注销失败',
            text: error.response ? error.response.data.message : '发生错误，请重试',
            icon: 'error'
          });
        }
      }
    };

    return {
      userInfo,
      reset,
      logout
    };
  },
};
</script>

<style scoped>
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
</style>