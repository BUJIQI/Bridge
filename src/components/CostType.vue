<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">产品成本类型核算报告（第{{ selectedCycle }}周期）</h3>
        <div class="cycle-selection" style="float: right;">
          <span>选择周期：</span>
          <select v-model="selectedCycle" @change="updateCycle">
            <option 
              v-for="cycle in historyCyclesToDisplay" 
              :key="cycle" 
              :value="cycle">
              第{{ cycle }}周期
            </option>
          </select>
        </div>
      </div>

      <div class="panel-body">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>成本类型</th>
                <th>百万元</th>
                <th>成本类型说明</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td colspan="3" class="subheader">材料费用</td>
              </tr>
              <tr>
                <td>原材料</td>
                <td>{{ currentReportData[0] }}</td>
                <td>直接成本</td>
              </tr>
              <tr>
                <td>附件</td>
                <td>{{ currentReportData[1] }}</td>
                <td>直接成本</td>
              </tr>
              <tr>
                <td>生产材料</td>
                <td>{{ currentReportData[2] }}</td>
                <td>直接成本</td>
              </tr>
              <tr>
                <td colspan="3" class="subheader">人员费用</td>
              </tr>
              <tr>
                <td>工资费用</td>
                <td>{{ currentReportData[3] }}</td>
                <td>{{ currentReportData[4] }}</td>
              </tr>
              <tr>
                <td>人员附加费用</td>
                <td>{{ currentReportData[5] }}</td>
                <td>{{ currentReportData[6] }}</td>
              </tr>
              <tr>
                <td>招聘/解雇费用</td>
                <td>{{ currentReportData[7] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td colspan="3" class="subheader">折旧费用</td>
              </tr>
              <tr>
                <td>厂房</td>
                <td>{{ currentReportData[8] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>生产线</td>
                <td>{{ currentReportData[9] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>机器人</td>
                <td>{{ currentReportData[10] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td colspan="3" class="subheader">其它经营费用</td>
              </tr>
              <tr>
                <td>其它固定费用</td>
                <td>{{ currentReportData[11] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>维修保养</td>
                <td>{{ currentReportData[12] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>合理化</td>
                <td>{{ currentReportData[13] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>返修/废品</td>
                <td>{{ currentReportData[14] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>库存费用</td>
                <td>{{ currentReportData[15] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>广告费用</td>
                <td>{{ currentReportData[16] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>市场研究</td>
                <td>{{ currentReportData[17] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td>其它研究开发费用</td>
                <td>{{ currentReportData[18] }}</td>
                <td>间接成本</td>
              </tr>
              <tr>
                <td class="summary" style="text-align: left;">合计：</td>
                <td class="summary">{{ currentReportData[19] }}</td>          
                <td class="summary"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
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
    const userInfo = userStore.userInfo;


    const historyCyclesToDisplay = [];
    for (let i = 1; i < userInfo.cycle; i++) {
      historyCyclesToDisplay.push(i);
    }

    const selectedCycle = ref(userInfo.cycle - 1);

    const reportData = ref({});

    const fetchReportData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/enterreporting/', {
            withCredentials: true
      });
        reportData.value = response.data['产品成本类型核算报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`产品成本类型核算报告（第${selectedCycle.value}周期）`] || [];
    });    


    const updateCycle = (event) => {
      selectedCycle.value = event.target.value; 
    };

    onMounted(() => {
      fetchReportData();
    });


    return {
      userInfo,
      historyCyclesToDisplay,
      selectedCycle,
      reportData,
      updateCycle,
      currentReportData
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

.cycle-selection {
    display: flex;
    align-items: center;
}

.cycle-selection select {
    cursor: pointer;
    padding: 10px; 
    border: 1px solid #ccc; 
    border-radius: 5px; 
    background-color: #fff; 
    color: #333; 
    font-size: 16px; 
    transition: border-color 0.3s; 
}

.cycle-selection select:hover {
    border-color: #c0392b; 
}

.cycle-selection select:focus {
    border-color: #c0392b; 
    outline: none; 
    box-shadow: 0 0 5px rgba(192, 57, 43, 0.5); 
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

.subheader {
  background-color: #f15d4f;
  color: #fff;
  text-align: left;
}

.summary {
  background-color: #c0392b;
  color: #fff;
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
}

td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
</style>
