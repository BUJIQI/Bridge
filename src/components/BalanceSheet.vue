<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">资产负债表（第{{ selectedCycle }}周期）</h3>
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
                <th colspan="2" style="border-right: 1px solid #ddd;">资产（百万元）</th>
                <th colspan="2">负债（百万元）</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td colspan="2" class="subheader" style="border-right: 1px solid #ddd;">固定资产</td>
                <td colspan="2" class="subheader">自有资金</td>
              </tr>
              <tr>
                <td colspan="2" style="text-align: left; border-right: 1px solid #ddd;">实物</td>
                <td>注册资金</td>
                <td>1000</td>
              </tr>
              <tr>
                <td>地产和厂房</td>
                <td style="border-right: 1px solid #ddd;">1150</td>
                <td>资金储备</td>
                <td>1000</td>
              </tr>
              <tr>
                <td>设备和生产设施</td>
                <td style="border-right: 1px solid #ddd;">1150</td>
                <td>利润储备</td>
                <td>1000</td>
              </tr>
              <tr>
                <td colspan="2" class="subheader" style="border-right: 1px solid #ddd;">流动资产</td>
                <td>前周期亏损结转</td>
                <td>1000</td>
              </tr>
              <tr>
                <td colspan="2" style="text-align: left; border-right: 1px solid #ddd;">库存</td>
                <td>周期结余/周期亏损</td>
                <td>1000</td>
              </tr>
              <tr>
                <td>原材料和附件</td>
                <td style="border-right: 1px solid #ddd;">10.04</td>
                <td colspan="2" class="subheader">债务</td>
              </tr>
              <tr>
                <td>成品</td>
                <td style="border-right: 1px solid #ddd;">32.4</td>
                <td colspan="2" style="text-align: left;">贷款</td>
              </tr>
              <tr>
                <td style="text-align: left;">债权</td>
                <td style="border-right: 1px solid #ddd;">4</td>
                <td>长期贷款</td>
                <td>1000</td>
              </tr>
              <tr>
                <td style="text-align: left;">有价证券</td>
                <td style="border-right: 1px solid #ddd;">4</td>
                <td>中期贷款</td>
                <td>1000</td>
              </tr>
              <tr>
                <td style="text-align: left;">现金</td>
                <td style="border-right: 1px solid #ddd;">4</td>
                <td>透支贷款</td>
                <td>1000</td>
              </tr>
              <tr>
                <td class="subheader">资产合计</td>
                <td class="subheader" style="text-align: center; border-right: 1px solid #ddd;">1150</td>
                <td class="subheader">负债合计</td>           
                <td class="subheader" style="text-align: center;">1000</td>
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
        reportData.value = response.data['资产负债表'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`资产负债表（第${selectedCycle.value}周期）`] || [];
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
