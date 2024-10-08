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
        <swal v-if="loginResult" title="提示" :text="loginResult.text" :icon="loginResult.icon"></swal>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios'; 
import { useRouter } from 'vue-router';

export default {
    setup() {
        const router = useRouter();
        const username = ref('');
        const password = ref('');
        const loginResult = ref('');

        const login = async () => {
            const payload = { username: username.value, password: password.value };
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/login/', payload);
                if (response.data.status === 'True') {
                    router.push('/main/'); // 登录成功后跳转到主页
                } else {
                    loginResult.value = {
                        text: response.data.data.logintxt, // 显示登录失败的信息
                        icon: 'error'
                    };
                }
            } catch (error) {
                loginResult.value = {
                    text: '登录失败，请重试！', // 设置错误提示
                    icon: 'error'
                };
            }
        };

        const goToRegister = () => {
            router.push('/register/'); // 跳转到注册
        };

        return {
            username,
            password,
            loginResult,
            login,
            goToRegister,
        };
    },
};
</script>

<style>
@import '@/assets/styles/L&R.css';
</style>
