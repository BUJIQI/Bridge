<template>
    <div class="register-container">
      <h2>用户注册</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="password">密码:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
  
        <div class="form-group">
          <button type="submit">注册</button>
        </div>
  
        <p v-if="message">{{ message }}</p>
      </form>
    </div>
  </template>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: '',  // 用于显示注册结果
    };
  },
  methods: {
    async submitForm() {
      try {
        // 向后端发送 POST 请求
        const response = await axios.post('http://127.0.0.1:8000/users/register/', 
        {
          username: this.username,
          password: this.password
        });
        
        // 根据返回的结果显示消息
        this.message = response.data.message;
      } catch (error) {
        // 错误处理
        if (error.response) {
          this.message = error.response.data.message;
        } else {
          this.message = '请求失败，请稍后再试';
        }
      }
    }
  }
};
</script>

  
  <style scoped>
  .register-container {
    width: 300px;
    margin: 0 auto;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  form button {
    padding: 10px 20px;
    cursor: pointer;
  }
  </style>
  