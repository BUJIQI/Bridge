<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">财务报告（第{{ selectedCycle }}周期）</h3>
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
                <th>现金收入</th>
                <th style="border-right: 1px solid #ddd;">本周期（百万元）</th>
                <th>现金支出 </th>
                <th>本周期（百万元）</th>
              </tr>
            </thead>
            <tbody>
                <tr class="highlight">  
                <td>期初现金</td>
                <td colspan="3">{{ currentReportData[0] }}</td>
              </tr>
              <tr>
                <td>本周期产品销售收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[1] }}</td>
                <td>材料费用</td>
                <td>{{ currentReportData[2] }}</td>
              </tr>
              <tr>
                <td>+ 前周期产品销售收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[3] }}</td>
                <td>+ 人员费用</td>
                <td>{{ currentReportData[4] }}</td>
              </tr>
              <tr>
                <td></td>
                <td style="border-right: 1px solid #ddd;"></td>
                <td>+ 其它经营费用</td>
                <td>{{ currentReportData[5] }}</td>
              </tr>
              <tr>
                <td>+ 有价证券</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[6] }}</td>
                <td>+ 中期和透支贷款归还</td>
                <td>{{ currentReportData[7] }}</td>
              </tr>
              <tr>
                <td>+ 利息收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[8] }}</td>
                <td>+ 利息费用</td>
                <td>{{ currentReportData[9] }}</td>
              </tr>
              <tr>
                <td></td>
                <td style="border-right: 1px solid #ddd;"></td>
                <td>+ 购买机器人</td>
                <td>{{ currentReportData[10] }}</td>
              </tr>
              <tr>
                <td>+ 特别收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[11] }}</td>
                <td>+ 购买生产线和厂房</td>
                <td>{{ currentReportData[12] }}</td>
              </tr>
              <tr>
                <td>+ 生产线变卖收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[13] }}</td>
                <td>+ 购买有价证券</td>
                <td>{{ currentReportData[14] }}</td>
              </tr>
              <tr>
                <td></td>
                <td style="border-right: 1px solid #ddd;"></td>
                <td>+ 税收</td>
                <td>{{ currentReportData[15] }}</td>
              </tr>
              <tr>
                <td>+ 中期贷款</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[16] }}</td>
                <td>+ 股息支付（前周期）</td>
                <td>{{ currentReportData[17] }}</td>
              </tr>
              <tr>
                <td>+ 透支贷款</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[18] }}</td>
                <td>+ 特别费用</td>
                <td>{{ currentReportData[19] }}</td>
              </tr>
              <tr>
                <td>+ 现金收入合计</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[20] }}</td>
                <td>+ 现金支出合计</td>
                <td>{{ currentReportData[21] }}</td>
              </tr>
              <tr class="highlight">
                <td>期末现金</td>
                <td colspan="3">{{ currentReportData[22] }}</td>
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
        reportData.value = response.data['财务报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`财务报告（第${selectedCycle.value}周期）`] || [];
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
  
  table {
    width: 100%;
    border-collapse: collapse;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); 
  }
  
  .highlight {
    background-color: #f15d4f;
    color: #fff;
  }
  
  th {
    background-color: #656464;
    color: #fff;
    text-align: center;
    padding: 20px;
  }
  
  td {
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
  }
</style>
  