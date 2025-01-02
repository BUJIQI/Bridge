<template>
  <div class="panel panel-default mt-3">
      <div class="panel-heading">
          <h3 class="panel-title">{{ matchingKey }}</h3> 
      </div>
      <div class="panel-body">
        <table class="table table-striped">
          <tbody>
            <tr v-for="(value, key) in filteredData" :key="key">
              <td class="highlight">{{ key }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '@/store/user';
import axios from 'axios';

export default {
  setup() {
      const userStore = useUserStore();
        userStore.setSelectedHistory(localStorage.getItem('SelectedPeriod'));
        
      const selectedHistory = computed(() => userStore.selectedHistory);  
      const Data = ref({}); 

      const fetchData = async () => {
          try {
              const response = await axios.get('http://127.0.0.1:8000/users/look1/', {
                  withCredentials: true
              });
              Data.value = response.data; 
              console.log('获取周期形势数据成功:', Data.value);
          } catch (error) {
              console.error('获取周期形势数据时发生错误:', error);
          }
      };

      // 在组件挂载时请求数据
      onMounted(() => {
          fetchData();
      });

      // 计算属性：检查是否存在 selectedHistory 字段对应的数据
      const matchingKey = computed(() => {
          return Object.keys(Data.value).find(key => key.includes(selectedHistory.value));
      });

      // 计算属性：返回过滤后的数据
      const filteredData = computed(() => {
          const dataEntries = Object.entries(Data.value[matchingKey.value] || {});
          return dataEntries.slice(1).reduce((acc, [key, value]) => {
              acc[key] = value;
              return acc;
          }, {});
      });

      return {
          Data,
          matchingKey,
          filteredData,
          selectedHistory
      };
  }
}
</script>

<style scoped>
.panel {
  margin-top: 20px;
  border-radius: 8px;
}

.panel-heading {
  background-color: #f7f7f9;
  padding: 15px;
}

.panel-body {
  padding: 20px;
  border-radius: 8px;
}

.table-striped > tbody > tr:nth-child(odd) {
  background-color: #f9f9f9;
  border-radius: 5px;
}

.highlight {
    background-color: #f3776c;
    color: #fff;
}
</style>
