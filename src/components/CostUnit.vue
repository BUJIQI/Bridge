<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">成本承担单位核算报告（第{{ selectedCycle }}周期）</h3>
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
                <th class="diagonal-header">
                    <span class="bottom-left">成本</span>
                    <span class="top-right">成本承担单元</span>
                </th>
                <th>合计（百万元）</th>
                <th>一般产品 一般市场</th>
                <th>一般产品 附加市场I</th>
                <th>特殊产品 附加市场II</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>原材料</td>
                <td>{{ currentReportData[0] }}</td>
                <td>{{ currentReportData[1] }}</td>
                <td>{{ currentReportData[2] }}</td>
                <td>{{ currentReportData[3] }}</td>
              </tr>
              <tr>
                <td>+ 附件</td>
                <td>{{ currentReportData[4] }}</td>
                <td>{{ currentReportData[5] }}</td>
                <td>{{ currentReportData[6] }}</td>
                <td>{{ currentReportData[7] }}</td>
              </tr>
              <tr>
                <td>+ 生产材料</td>
                <td>{{ currentReportData[8] }}</td>
                <td>{{ currentReportData[9] }}</td>
                <td>{{ currentReportData[10] }}</td>
                <td>{{ currentReportData[11] }}</td>
              </tr>
              <tr>
                <td>= 材料直接费用</td>
                <td>{{ currentReportData[12] }}</td>
                <td>{{ currentReportData[13] }}</td>
                <td>{{ currentReportData[14] }}</td>
                <td>{{ currentReportData[15] }}</td>
              </tr>
              <tr>
                <td>+ 材料间接费用</td>
                <td>{{ currentReportData[16] }}</td>
                <td>{{ currentReportData[17] }}</td>
                <td>{{ currentReportData[18] }}</td>
                <td>{{ currentReportData[19] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 材料成本</td>
                <td>{{ currentReportData[20] }}</td>
                <td>{{ currentReportData[21] }}</td>
                <td>{{ currentReportData[22] }}</td>
                <td>{{ currentReportData[23] }}</td>
              </tr>
              <tr>
                <td>加工直接费用</td>
                <td>{{ currentReportData[24] }}</td>
                <td>{{ currentReportData[25] }}</td>
                <td>{{ currentReportData[26] }}</td>
                <td>{{ currentReportData[27] }}</td>
              </tr>
              <tr>
                <td>+ 加工间接费用</td>
                <td>{{ currentReportData[28] }}</td>
                <td>{{ currentReportData[29] }}</td>
                <td>{{ currentReportData[30] }}</td>
                <td>{{ currentReportData[31] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 加工成本</td>
                <td>{{ currentReportData[32] }}</td>
                <td>{{ currentReportData[33] }}</td>
                <td>{{ currentReportData[34] }}</td>
                <td>{{ currentReportData[35] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 制造成本</td>
                <td>{{ currentReportData[36] }}</td>
                <td>{{ currentReportData[37] }}</td>
                <td>{{ currentReportData[38] }}</td>
                <td>{{ currentReportData[39] }}</td>
              </tr>
              <tr>
                <td>+ 研究开发费用</td>
                <td>{{ currentReportData[40] }}</td>
                <td>{{ currentReportData[41] }}</td>
                <td>{{ currentReportData[42] }}</td>
                <td>{{ currentReportData[43] }}</td>
              </tr>
              <tr>
                <td>+ 销售费用</td>
                <td>{{ currentReportData[44] }}</td>
                <td>{{ currentReportData[45] }}</td>
                <td>{{ currentReportData[46] }}</td>
                <td>{{ currentReportData[47] }}</td>
              </tr>
              <tr>
                <td>+ 管理费用</td>
                <td>{{ currentReportData[48] }}</td>
                <td>{{ currentReportData[49] }}</td>
                <td>{{ currentReportData[50] }}</td>
                <td>{{ currentReportData[51] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 产品成本</td>
                <td>{{ currentReportData[52] }}</td>
                <td>{{ currentReportData[53] }}</td>
                <td>{{ currentReportData[54] }}</td>
                <td>{{ currentReportData[55] }}</td>
              </tr>
              <tr>
                <td>销售收入</td>
                <td>{{ currentReportData[56] }}</td>
                <td>{{ currentReportData[57] }}</td>
                <td>{{ currentReportData[58] }}</td>
                <td>{{ currentReportData[59] }}</td>
              </tr>
              <tr>
                <td>+/- 产品库存变化</td>
                <td>{{ currentReportData[60] }}</td>
                <td>{{ currentReportData[61] }}</td>
                <td>{{ currentReportData[62] }}</td>
                <td>{{ currentReportData[63] }}</td>
              </tr>
              <tr class="highlight">
                <td>= 总的经营收入</td>
                <td>{{ currentReportData[64] }}</td>
                <td>{{ currentReportData[65] }}</td>
                <td>{{ currentReportData[66] }}</td>
                <td>{{ currentReportData[67] }}</td>
              </tr>
              <tr class="summary">
                <td>生产经营成果</td>
                <td>{{ currentReportData[68] }}</td>
                <td>{{ currentReportData[69] }}</td>
                <td>{{ currentReportData[70] }}</td>
                <td>{{ currentReportData[71] }}</td>
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
        reportData.value = response.data['成本承担单元核算报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`成本承担单元核算报告（第${selectedCycle.value}周期）`] || [];
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

  .summary {
    background-color: #c0392b;
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
  
  .diagonal-header {
    position: relative;
  }
  
  .diagonal-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 108%;
    height: 1px;
    background: rgb(179, 179, 179);
    transform: rotate(23deg);
    transform-origin: top left;
  }
  
  .bottom-left {
    position: absolute;
    bottom: 5px;
    left: 5px; 
  }
  
  .top-right {
    position: absolute;
    top: 5px;
    right: 5px;
    white-space: nowrap;
  }
</style>
  