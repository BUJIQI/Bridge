<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>   
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">利润和亏损核算报告（第{{ selectedCycle }}周期）</h3>
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
                <th></th>
                <th style="border-right: 1px solid #ddd;">百万元</th>
                <th></th>
                <th>百万元</th>
              </tr>
            </thead>
            <tbody>
              <tr class="highlight">
                <td>销售收入</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[0] }}</td>
                <td>销售收入</td>
                <td>{{ currentReportData[1] }}</td>
              </tr>
              <tr>
                <td>+/- 产品库存变化</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[2] }}</td>
                <td rowspan="2">- 销售产品制造成本</td>
                <td rowspan="2">{{ currentReportData[3] }}</td>
              </tr>
              <tr>
                <td>- 材料费用</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[4] }}</td>
              </tr>
              <tr>
                <td>- 人员费用</td>
                <td style="border-right: 1px solid #ddd;"></td>
                <td rowspan="2">- 销售费用</td>
                <td rowspan="2">{{ currentReportData[5] }}</td>
              </tr>
              <tr>
                <td>- 工资</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[6] }}</td>
              </tr>
              <tr>
                <td>- 人员附加费用</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[7] }}</td>
                <td rowspan="2">- 研究开发费用</td>
                <td rowspan="2">{{ currentReportData[8] }}</td>
              </tr>
              <tr>
                <td>- 其它人员费用</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[9] }}</td>
              </tr>
              <tr>
                <td>- 折旧</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[10] }}</td>
                <td rowspan="2">- 管理费用</td>
                <td rowspan="2">{{ currentReportData[11] }}</td>
              </tr>
              <tr>
                <td>- 其它经营费用</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[12] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 生产经营成果</td>
                <td style="border-right: 1px solid #ddd;">{{ currentReportData[13] }}</td>
                <td>= 生产经营成果</td>
                <td>{{ currentReportData[14] }}</td>
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
        reportData.value = response.data['利润和亏损核算报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`利润和亏损核算报告（第${selectedCycle.value}周期）`] || [];
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
  