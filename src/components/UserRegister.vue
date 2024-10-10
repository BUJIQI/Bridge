<template>
    <div class="container">
        <h2>注册</h2>
        <form @submit.prevent="register">
            <input type="text" v-model="className" placeholder="班级" required>
            <input type="text" v-model="studentID" placeholder="学号" required>
            <input type="text" v-model="name" placeholder="姓名" required>
            <input type="text" v-model="teamName" placeholder="队名" required>
            <input type="password" v-model="password" placeholder="密码" required>
            <input type="tel" v-model="phone" placeholder="手机号" required>
            <div class="button-container">
                <button type="button" @click="goToLogin">返回登录</button>
                <button type="submit" id="register-btn">注册</button>
            </div>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'; // 引入原生 SweetAlert2
        
export default {
    setup() {
        const router = useRouter();       
        const className = ref('');
        const studentID = ref('');
        const name = ref('');
        const teamName = ref('');
        const password = ref('');
        const phone = ref('');
        
        const register = async () => {
            const payload = {
                classid: className.value,
                studentid: studentID.value,
                name: name.value,
                teamname: teamName.value,
                pwd: password.value,
                phone: phone.value
            };
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/register/', payload);
                if (response.data.status === 'True') {
                    const group = response.data.data.group;
                    const number = response.data.data.number;
                    Swal.fire({
                        title: '提示',
                        text: `注册成功，编号为第${group}组第${number}企业！`,
                        icon: 'success'
                    });
                    setTimeout(goToLogin, 4000); // 注册成功后跳转到登录页
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
        
        const goToLogin = () => {
            router.push('/login/');
        };
        
        return {
            className,
            studentID,
            name,
            teamName,
            password,
            phone,
            register,
            goToLogin,
        };
    },
};
</script>

<style>
@import '@/assets/styles/L&R.css';
</style>
