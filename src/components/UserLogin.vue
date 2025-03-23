<template>
  <div class="auth-container">
    <div class="container">
      <div class="row h-100">
        <div class="col-md-8 left-section">
          <div class="logo">
            <img src="@/assets/logo.gif" alt="ICEDSS" />
            <span>JCTD</span>
          </div>
          <div class="full-name">
            <h1>现代企业创业决策仿真系统</h1>
            <p>欢迎来到我们的平台，开始您的创业决策之旅。</p>
          </div>
        </div>
        <div class="col-md-4 right-section">
          <div v-if="isLogin">
            <h2 class="mb-4">登录</h2>
            <hr>
            <form @submit.prevent="login">
              <div class="mb-3 row">
                <label for="username" class="col-sm-3 col-form-label">学号:</label>
                <div class="col-sm-9">
                  <input type="text" id="username" v-model="username" class="form-control" required />
                </div>
              </div>
              <div class="mb-3 row">
                <label for="password" class="col-sm-3 col-form-label">密码:</label>
                <div class="col-sm-9">
                  <input type="password" id="password" v-model="password" class="form-control" required />
                </div>
              </div>
              <p>新用户请先点击注册！</p>
              <div class="button-container text-center">
                <button type="submit" class="btn btn-primary me-2">登录</button>
                <button type="button" class="btn btn-secondary" @click="toggleForm">注册</button>
              </div>
            </form>
          </div>
          <div v-else>
            <h2 class="mb-4">注册</h2>
            <hr>
            <form @submit.prevent="register">
              <div class="mb-3 row">
                <label for="className" class="col-sm-3 col-form-label">班级:</label>
                <div class="col-sm-9">
                  <input type="text" id="className" v-model="className" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="studentID" class="col-sm-3 col-form-label">学号:</label>
                <div class="col-sm-9">
                  <input type="text" id="studentID" v-model="studentID" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="name" class="col-sm-3 col-form-label">姓名:</label>
                <div class="col-sm-9">
                  <input type="text" id="name" v-model="name" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="teamName" class="col-sm-3 col-form-label">队名:</label>
                <div class="col-sm-9">
                  <input type="text" id="teamName" v-model="teamName" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="password" class="col-sm-3 col-form-label">密码:</label>
                <div class="col-sm-9">
                  <input type="password" id="password" v-model="password" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="phone" class="col-sm-3 col-form-label">手机:</label>
                <div class="col-sm-9">
                  <input type="tel" id="phone" v-model="phone" class="form-control" required>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="email" class="col-sm-3 col-form-label">邮箱:</label>
                <div class="col-sm-9">
                  <input type="email" id="email" v-model="email" class="form-control" required>
                </div>
              </div>
              <div class="button-container text-center">
                <button type="button" class="btn btn-secondary me-2" @click="toggleForm">返回登录</button>
                <button type="submit" class="btn btn-primary" id="register-btn">注册</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from '@/api/axios';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import { useUserStore } from '@/store/user';

export default {
  setup() {
    const router = useRouter();
    const userStore = useUserStore();
    const isLogin = ref(true);

    const username = ref('');
    const password = ref('');
    const className = ref('');
    const studentID = ref('');
    const name = ref('');
    const teamName = ref('');
    const phone = ref('');
    const email = ref('');

    const login = async () => {
      const payload = { username: username.value, password: password.value };
      try {
        const response = await axios.post('/users/login/', payload, {
          withCredentials: true,
        });

        if (response.data.status === 'True') {
          userStore.setUserInfo(response.data.data);
          localStorage.setItem('isLoggedIn', 'true');
          localStorage.setItem('userInfo', JSON.stringify(response.data.data));
          router.push('/');
        } else {
          Swal.fire({
            title: '提示',
            text: response.data.data.logintxt,
            icon: 'error',
          });
        }
      } catch (error) {
        Swal.fire({
          title: '提示',
          text: '登录失败，请重试！',
          icon: 'error',
        });
      }
    };

    const register = async () => {
      const payload = {
        classid: className.value,
        studentid: studentID.value,
        name: name.value,
        teamname: teamName.value,
        pwd: password.value,
        phone: phone.value,
        email: email.value
      };
      try {
        const response = await axios.post('/users/register/', payload, {
          withCredentials: true,
        });
        if (response.data.status === 'True') {
          const group = response.data.data.group;
          const number = response.data.data.number;
          Swal.fire({
            title: '提示',
            text: `注册成功，编号为第${group}组第${number}企业！`,
            icon: 'success'
          });
          setTimeout(() => {
            isLogin.value = true;
          }, 4000); // 注册成功后切换回登录表单
        } else {
          Swal.fire({
            title: '提示',
            text: response.data.data.registertxt || '未知错误', // 显示注册失败的信息
            icon: 'error'
          });
        }
      } catch (error) {
        console.error(error); // 记录错误信息
        Swal.fire({
          title: '提示',
          text: '注册失败，请重试！', // 设置错误提示
          icon: 'error'
        });
      }
    };

    const toggleForm = () => {
      isLogin.value = !isLogin.value;
    };

    return {
      isLogin,
      username,
      password,
      className,
      studentID,
      name,
      teamName,
      phone,
      email,
      login,
      register,
      toggleForm,
    };
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #fcfbfb, #ffc3a0);
  min-height: 100vh; 
}

.row {
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.logo img {
  width: 60px;
  height: 60px;
  margin-right: 20px;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.logo span {
  font-size: 35px;
  font-weight: bold;
  color: #6b5b5b;
  font-family: 'Times New Roman', Times, serif;
}

.full-name {
  margin-bottom: 30px;
}

.full-name h1 {
  color: #ff6b6b;
  margin-bottom: 15px;
  font-size: 50px;
}

.full-name p {
  margin: 0;
  font-size: 18px;
  color: #666;
}

.right-section {
  padding: 25px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  text-align: center;
  width: fit-content;
}

.right-section h2 {
  font-size: 28px;
  color: #ff6b6b;
}

.right-section p {
  color: #666;
  font-size: small;
}

button {
  width: 100px;
  margin: 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #ff6b6b;
  color: white;
}

.btn-primary:hover {
  background-color: #ff4d4d;
}

.btn-secondary {
  background-color: #ffadd2;
  color: #ff6b6b;
}

.btn-secondary:hover {
  background-color: #ffc3a0;
}
</style>