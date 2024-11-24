<template>
    <div class="container">
        <h2 class="mb-4">注册</h2>
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
            <div class="button-container text-center">
                <button type="button" class="btn btn-secondary me-2" @click="goToLogin">返回登录</button>
                <button type="submit" class="btn btn-primary" id="register-btn">注册</button>
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
            router.push('/');
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

<style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    position: absolute;
    top: 50%; 
    left: 50%; 
    transform: translate(-50%, -50%); 
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



