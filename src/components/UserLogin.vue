<template>
    <div class="container mt-5">
        <h2 class="mb-4">登录</h2>
        <form @submit.prevent="login">
            <div class="mb-3 row">
                <label for="username" class="col-sm-3 col-form-label">学号:</label>
                <div class="col-sm-9">
                    <input type="text" id="username" v-model="username" class="form-control"  required>
                </div>
            </div>
            <div class="mb-3 row">
                <label for="password" class="col-sm-3 col-form-label">密码:</label>
                <div class="col-sm-9">
                    <input type="password" id="password" v-model="password" class="form-control"  required>
                </div>
            </div>
            <p>新用户请先点击注册！</p>
            <div class="button-container text-center">
                <button type="submit" class="btn btn-primary me-2">登录</button>
                <button type="button" class="btn btn-secondary" @click="goToRegister">注册</button>
            </div>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue'; 
import axios from 'axios'; 
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'; 
import { useUserStore } from '@/store/user'; 

export default {
    setup() { 
        const router = useRouter();
        const userStore = useUserStore();
        const username = ref('');
        const password = ref('');

        const login = async () => {
            const payload = { username: username.value, password: password.value };
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/login/', payload);
                if (response.data.status === 'True') {
                    userStore.setUserInfo(response.data.data);
                    router.push('/decision'); 
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

        const goToRegister = () => {
            router.push('/register/'); 
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
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    width: 300px;
    padding: 20px;
    background-color: white;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    text-align: center;
}

button {
    width: 100px;
    padding: 10px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>



