<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，不得显示评价总表</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">各企业生产经营决策<strong>综合</strong>评价表</h3>
      </div>

      <div class="panel-body">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th rowspan="2">项目</th>
                <th rowspan="2">企业</th>
                <th colspan="8">周期</th>
              </tr>
              <tr>
                <th>1</th>
                <th>2</th>
                <th>3</th>
                <th>4</th>
                <th>5</th>
                <th>6</th>
                <th>7</th>
                <th>评分</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(item, index) in OverallData" :key="index">                
                <tr>
                    <td rowspan="2">经营决策综合评价<br>（分数名次）</td>
                    <td>计算机</td>
                    <td v-for="(value, i) in item.computerValues" :key="i">{{ value }}</td>
                </tr>
                <tr class="highlight">
                    <td>本企业</td>
                    <td v-for="(value, i) in item.enterpriseValues" :key="i">{{ value }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/store/user';
import axios from 'axios';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;

    const OverallData = ref([
      {
        computerValues: [],
        enterpriseValues: []
      },
    ]);

    const fetchReportData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/summart_evaluation/', {
          withCredentials: true
        });
        
        const OverallDataArray = response.data['决策综合评价'];

        OverallData.value[0].computerValues = OverallDataArray.slice(0, 8);
        OverallData.value[0].enterpriseValues = OverallDataArray.slice(8);

      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    onMounted(() => {
      fetchReportData();
    });

    return {
      userInfo,
      OverallData,
    };
  },
};
</script>

<style scoped>
.no-report-message {
  display: flex; 
  justify-content: center; 
  align-items: center; 
  height: calc(100vh - 100px); 
  font-size: 50px; 
  color: #333; 
  font-weight: bold; 
  text-align: center;
}

.panel {
  margin-top: 20px;
  border-radius: 8px;
}

.panel-heading {
  background-color: #f7f7f9;
  padding: 15px;
  display: flex; 
  justify-content: space-between; 
  align-items: center;
}

.panel-body {
  padding: 20px;
  border-radius: 8px;
}

.table-container {
  background-color: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); 
}

.highlight {
  background-color: #f9cfcb;
}

table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); 
}

th {
  background-color: #656464;
  color: #fff;
  text-align: center;
  padding: 8px;
  border: 1px solid #ddd;
}

td {
  padding: 8px;
  text-align: center;
  border: 1px solid #ddd;
}
</style>
