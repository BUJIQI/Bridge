<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useUserStore } from '@/store/user';

export default {
  name: 'App',
  setup() {
    const userStore = useUserStore(); 

    onMounted(() => {
      const isLoggedIn = sessionStorage.getItem('isLoggedIn');
      if (isLoggedIn) {
        userStore.setUserInfo(JSON.parse(sessionStorage.getItem('userInfo'))); 
        if (sessionStorage.getItem('newcycle')) {
          userStore.userInfo.cycle = Number(sessionStorage.getItem('newcycle'));       
        }
      }
    });

    return {};
  },  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>