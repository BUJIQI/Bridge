<template>
  <div class="auth-container">
    <div class="container">
      <div class="row head h-100">
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
            <form @submit.prevent="login" novalidate class="needs-validation">
              <input type="text" id="username" v-model="username" class="form-control form-control-sm input-login" placeholder="请输入学号" required maxlength="15"/>
              <input type="password" id="password" v-model="password" class="form-control form-control-sm input-login" placeholder="请输入密码" required/>
              <div class="button-container text-center">
                <button type="submit" class="btn btn-primary me-2">登录</button>
              </div>
              <div class="d-flex justify-content-center">
                <a href="#" @click.prevent="toggleForm">还没有账号？点击注册</a>
              </div>
            </form>
          </div>
          <div v-else>
            <h2 class="mb-4">注册</h2>
            <form @submit.prevent="register" novalidate class="needs-validation">
              <div class="mb-3 row">
                <label for="className" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">班级</label>
                <div class="col-sm-10">
                  <input type="text" id="className" v-model="className" class="form-control" required maxlength="20">
                </div>
              </div>
              <div class="mb-3 row">
                <label for="studentID" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">学号</label>
                <div class="col-sm-10">
                  <input type="text" id="studentID" v-model="studentID" class="form-control" required maxlength="15">
                </div>
              </div>
              <div class="mb-3 row">
                <label for="name" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">姓名</label>
                <div class="col-sm-10">
                  <input type="text" id="name" v-model="name" class="form-control" required maxlength="20">
                </div>
              </div>
              <div class="mb-3 row">
                <label for="teamName" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">队名</label>
                <div class="col-sm-10">
                  <input type="text" id="teamName" v-model="teamName" class="form-control" required maxlength="16">
                </div>
              </div>
              <div class="mb-3 row">
                <label for="password" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">密码</label>
                <div class="col-sm-10">
                  <input type="password" id="password" v-model="password" class="form-control" required maxlength="5">
                </div>
              </div>
              <div class="mb-3 row">
                <label for="phone" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">手机</label>
                <div class="col-sm-10">
                  <input type="tel" id="phone" v-model="phone" pattern="\d{11}" maxlength="11" class="form-control" required>
                  <div class="invalid-feedback">
                    手机号必须是11位数字。
                  </div>
                </div>
              </div>
              <div class="mb-3 row">
                <label for="email" class="col-sm-2 col-form-label" style="font-size: 0.87rem;">邮箱</label>
                <div class="col-sm-10">
                  <input type="email" id="email" v-model="email" class="form-control" required>
                  <div class="invalid-feedback">
                    请输入有效的邮箱地址。
                  </div>
                </div>
              </div>
              <div class="button-container text-center">
                <button type="submit" class="btn btn-primary" id="register-btn">注册</button>
              </div>
              <div class="d-flex justify-content-center">
                <a href="#" @click.prevent="toggleForm">已有账号？点击登录</a>
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

    const login = async (event) => {
      const form = event.target.closest('form');
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return; // 确保只有在验证通过的情况下才继续执行
      }
      form.classList.add('was-validated');

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

    const register = async (event) => {
      const form = event.target.closest('form');
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return; // 确保只有在验证通过的情况下才继续执行
      }
      form.classList.add('was-validated');

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
  background: linear-gradient(180deg, #e7e7e7, #fbe4e4);
  min-height: 100vh; 
}

.head {
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
  color: #424242;
  font-family: 'Times New Roman', Times, serif;
}

.full-name {
  margin-bottom: 30px;
}

.full-name h1 {
  color: #ac0c0c;
  margin-bottom: 15px;
  font-size: 50px;
  font-weight: bold;
  font-family: 'Noto Serif SC', serif;
}

.full-name p {
  margin: 0;
  font-size: 18px;
  color: #252424;
}

.right-section {
  padding: 25px;
  background-color: rgba(159, 159, 159, 0.416);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.right-section h2 {
  font-size: 28px;
  color: #bf3535;
  text-align: center;
  font-weight: bold;
}

.input-login {
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 20px;
}

.d-flex a {
  text-decoration: none; 
  color: #3b2f2f; 
  font-size: 0.8rem; 
}

.d-flex a:hover {
  color: #201919; 
}

button {
  width: 100%;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 10px;
  margin-bottom: 20px;
}

.btn-primary {
  background-color: #d13939;
  color: white;
}

.btn-primary:hover {
  background-color: #a72f2f;
}
</style>
