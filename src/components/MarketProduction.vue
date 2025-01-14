<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">市场生产数据报表（第{{ selectedCycle }}周期）</h3>
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
            <div class="header">市场报告</div>
            <table>
              <thead>
                <tr>
                  <th rowspan="2"></th>
                  <th rowspan="2">一般市场</th>
                  <th colspan="2">附加市场</th>
                </tr>
                <tr>
                  <th>I</th>
                  <th>II</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>价格（元/台）</td>
                  <td>{{ currentReportData[0] }}</td>
                  <td>{{ currentReportData[1] }}</td>
                  <td>{{ currentReportData[2] }}</td>
                </tr>
                <tr>
                  <td>销售量（台）</td>
                  <td>{{ currentReportData[3] }}</td>
                  <td>{{ currentReportData[4] }}</td>
                  <td>{{ currentReportData[5] }}</td>
                </tr>
                <tr>
                  <td>销售额（百万元）</td>
                  <td>{{ currentReportData[6] }}</td>
                  <td>{{ currentReportData[7] }}</td>
                  <td>{{ currentReportData[8] }}</td>
                </tr>
                <tr>
                  <td>市场占有率（%）</td>
                  <td colspan="3">{{ currentReportData[9] }}</td>
                </tr>
                <tr>
                  <td>产品质量评价</td>
                  <td colspan="3">{{ currentReportData[10] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">仓库报告I：原材料</div>
            <table>
              <thead>
                <tr>
                  <th rowspan="2"></th>
                  <th rowspan="2">量（台）</th>
                  <th colspan="2">价值</th>
                </tr>
                <tr>
                  <th>（元/台）</th>
                  <th>（百万元）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>期初库存</td>
                  <td>{{ currentReportData[11] }}</td>
                  <td>{{ currentReportData[12] }}</td>
                  <td>{{ currentReportData[13] }}</td>
                </tr>
                <tr>
                  <td>+ 增加</td>
                  <td>{{ currentReportData[14] }}</td>
                  <td>{{ currentReportData[15] }}</td>
                  <td>{{ currentReportData[16] }}</td>
                </tr>
                <tr>
                  <td>- 消耗</td>
                  <td>{{ currentReportData[17] }}</td>
                  <td>{{ currentReportData[18] }}</td>
                  <td>{{ currentReportData[19] }}</td>
                </tr>
                <tr>
                  <td>= 期末库存</td>
                  <td>{{ currentReportData[20] }}</td>
                  <td>{{ currentReportData[21] }}</td>
                  <td>{{ currentReportData[22] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">仓库报告II：一般产品</div>
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>量（台）</th>
                  <th>制造成本（元/台）</th>
                  <th>库存价值（百万元）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>期初库存</td>
                  <td>{{ currentReportData[23] }}</td>
                  <td>{{ currentReportData[24] }}</td>
                  <td>{{ currentReportData[25] }}</td>
                </tr>
                <tr>
                  <td>+ 增加</td>
                  <td>{{ currentReportData[26] }}</td>
                  <td>{{ currentReportData[27] }}</td>
                  <td>{{ currentReportData[28] }}</td>
                </tr>
                <tr>
                  <td>- 消耗</td>
                  <td>{{ currentReportData[29] }}</td>
                  <td>{{ currentReportData[30] }}</td>
                  <td>{{ currentReportData[31] }}</td>
                </tr>
                <tr>
                  <td>= 期末库存</td>
                  <td>{{ currentReportData[32] }}</td>
                  <td>{{ currentReportData[33] }}</td>
                  <td>{{ currentReportData[34] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">仓库报告III：附件</div>
            <table>
              <thead>
                <tr>
                  <th rowspan="2"></th>
                  <th rowspan="2">量（台）</th>
                  <th colspan="2">价值</th>
                </tr>
                <tr>
                  <th>（元/台）</th>
                  <th>（百万元）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>期初库存</td>
                  <td>{{ currentReportData[35] }}</td>
                  <td>{{ currentReportData[36] }}</td>
                  <td>{{ currentReportData[37] }}</td>
                </tr>
                <tr>
                  <td>+ 增加</td>
                  <td>{{ currentReportData[38] }}</td>
                  <td>{{ currentReportData[39] }}</td>
                  <td>{{ currentReportData[40] }}</td>
                </tr>
                <tr>
                  <td>- 消耗</td>
                  <td>{{ currentReportData[41] }}</td>
                  <td>{{ currentReportData[42] }}</td>
                  <td>{{ currentReportData[43] }}</td>
                </tr>
                <tr>
                  <td>= 期末库存</td>
                  <td>{{ currentReportData[44] }}</td>
                  <td>{{ currentReportData[45] }}</td>
                  <td>{{ currentReportData[46] }}</td>
                </tr>
              </tbody>
            </table>
          </div>  
          
          <div class="table-container">
            <div class="header">人员报告I</div>
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>生产部门</th>
                  <th>研究开发部门</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>期初人员</td>
                  <td>{{ currentReportData[47] }}</td>
                  <td>{{ currentReportData[48] }}</td>
                </tr>
                <tr>
                  <td>+ 招聘</td>
                  <td>{{ currentReportData[49] }}</td>
                  <td>{{ currentReportData[50] }}</td>
                </tr>
                <tr>
                  <td>- 解雇</td>
                  <td>{{ currentReportData[51] }}</td>
                  <td>{{ currentReportData[52] }}</td>
                </tr>
                <tr>
                  <td>- 流动</td>
                  <td>{{ currentReportData[53] }}</td>
                  <td>{{ currentReportData[54] }}</td>
                </tr>
                <tr>
                  <td>= 期末人员</td>
                  <td>{{ currentReportData[55] }}</td>
                  <td>{{ currentReportData[56] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">人员报告II</div>
            <table>
              <thead>
                <tr>
                  <th>部门</th>
                  <th>人员（个）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>销售</td>
                  <td>{{ currentReportData[57] }}</td>
                </tr>
                <tr>
                  <td>采购</td>
                  <td>{{ currentReportData[58] }}</td>
                </tr>
                <tr>
                  <td>管理</td>
                  <td>{{ currentReportData[59] }}</td>
                </tr>
                <tr>
                  <td>管理的合理化系数</td>
                  <td>{{ currentReportData[60] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">生产报告I</div>
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>生产线（条）</th>
                  <th>机器人（个）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>前周期</td>
                  <td>{{ currentReportData[61] }}</td>
                  <td>{{ currentReportData[62] }}</td>
                </tr>
                <tr>
                  <td>+ 投资</td>
                  <td>{{ currentReportData[63] }}</td>
                  <td>{{ currentReportData[64] }}</td>
                </tr>
                <tr>
                  <td>- 变卖</td>
                  <td>{{ currentReportData[65] }}</td>
                  <td>{{ currentReportData[66] }}</td>
                </tr>
                <tr>
                  <td>本周期</td>
                  <td>{{ currentReportData[67] }}</td>
                  <td>{{ currentReportData[68] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">生产报告II</div>
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>加工（台）</th>
                  <th>设备要求（单位）</th>
                  <th>人员要求（个）</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>一般产品</td>
                  <td>{{ currentReportData[69] }}</td>
                  <td>{{ currentReportData[70] }}</td>
                  <td>{{ currentReportData[71] }}</td>
                </tr>
                <tr>
                  <td>特殊产品</td>
                  <td>{{ currentReportData[72] }}</td>
                  <td>{{ currentReportData[73] }}</td>
                  <td>{{ currentReportData[74] }}</td>
                </tr>
                <tr>
                  <td>合计</td>
                  <td>{{ currentReportData[75] }}</td>
                  <td>{{ currentReportData[76] }}</td>
                  <td>{{ currentReportData[77] }}</td>
                </tr>
                <tr>
                  <td>负载率（%）</td>
                  <td>{{ currentReportData[78] }}</td>
                  <td>{{ currentReportData[79] }}</td>
                  <td>{{ currentReportData[80] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">生产报告III</div>
            <table>
              <tbody>
                <tr>
                  <td>生产线的合理化系数</td>
                  <td>{{ currentReportData[81] }}</td>
                </tr>
                <tr>
                  <td>生产线维修保养系数</td>
                  <td>{{ currentReportData[82] }}</td>
                </tr>
                <tr>
                  <td>生产线负载率100%时生产能力</td>
                  <td>{{ currentReportData[83] }}</td>
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
import axios from '@/api/axios';

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
        const response = await axios.get('/users/enterreporting/', {
            withCredentials: true
      });
        reportData.value = response.data['市场生产数据报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`市场生产数据报告（第${selectedCycle.value}周期）`] || [];
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
  margin-bottom: 50px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); 
}

.header {
  background-color: #c0392b;
  color: #fff;
  padding: 10px;
  border-radius: 8px 8px 0 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #808080;
  color: #fff;
  text-align: center;
  padding: 8px;
  border: 1px solid #ddd;
}

td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
</style>
