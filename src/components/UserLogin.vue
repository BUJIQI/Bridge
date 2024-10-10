<template>
    <div class="container">
        <h2>登录</h2>
        <form @submit.prevent="login">
            <input type="text" v-model="username" placeholder="用户名" required>
            <input type="password" v-model="password" placeholder="密码" required>
            <p>新用户请先点击注册！</p>
            <div class="button-container">
                <button type="submit" id="login-btn">登录</button>
                <button type="button" id="register-btn" @click="goToRegister">注册</button>
            </div>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue'; 
import axios from 'axios'; 
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'; // 引入原生 SweetAlert2
import { useUserStore } from '@/store/user'; // 导入用户存储

export default {
    setup() { 
        const router = useRouter();
        const userStore = useUserStore();
        const username = ref('');
        const password = ref('');

        const login = async () => {
            const payload = { username: username.value, password: password.value };
            console.log('请求数据:', payload);
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/login/', payload);
                console.log('响应数据:', response.data);
                if (response.data.status === 'True') {
                    userStore.setUserInfo(response.data.data);
                    // 登录成功后跳转到主页
                    router.push('/main/'); 
                } else {
                    // 登录失败，使用 SweetAlert 显示提示
                    Swal.fire({
                        title: '提示',
                        text: response.data.data.logintxt,
                        icon: 'error',
                    });
                }
            } catch (error) {
                // 捕获错误，使用 SweetAlert 显示提示
                Swal.fire({
                    title: '提示',
                    text: '登录失败，请重试！',
                    icon: 'error',
                });
            }
        };

        const goToRegister = () => {
            router.push('/register/'); // 跳转到注册
        };

        return {
            username,
            password,
            login,
            goToRegister,
        };
    },
};
</script>

<style>
@import '@/assets/styles/L&R.css';
</style>

