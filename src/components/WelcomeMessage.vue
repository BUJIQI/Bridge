<template>
    <div class="container">
      <h1 class="title">欢迎来到现代企业创业决策仿真系统</h1>
      <h2 class="subtitle">——人机对抗版</h2>
    </div>
</template>
  
<script>
  export default {
    name: 'WelcomeMessage',
  };
</script>
  
<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f0f4f8;
    font-family: Arial, sans-serif;
  }
  
  .title {
    font-size: 36px;
    color: #333;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    margin: 10px 0;
  }
  
  .subtitle {
    font-size: 24px;
    color: #666;
    margin: 5px 0;
    padding: 0 10px;
    border-left: 3px solid #007BFF;
    padding-left: 10px;
    transition: color 0.3s;
  }
  
  .subtitle:hover {
    color: #007BFF;
  }
</style>
  