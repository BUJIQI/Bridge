<template>
    <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无报告可查看</div>
    <div v-else>
    <div class="panel panel-default mt-3">
      <div class="panel-heading">
        <h3 class="panel-title" v-if="currentReportData !== '本周期没有订购市场和生产研究报告！'">各企业市场营销及生产研究报告（第{{ selectedCycle }}周期）</h3>
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
      <div class="no-report-message" v-if="currentReportData === '本周期没有订购市场和生产研究报告！'">本周期没有订购市场和生产研究报告</div>
      <div v-else> 
      <div class="panel-body">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th colspan="2" style="width: 50%;">项目/企业</th>
                <th>1</th>
                <th>2</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in reportItems" :key="index">
                <td class="highlight">{{ item.label }}</td>
                <td class="highlight">{{ item.unit }}</td>
                <td>{{ currentReportData[index * 2] }}</td>
                <td>{{ currentReportData[index * 2 + 1] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
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

    const reportItems = ref([
        { label: '一般市场价格', unit: '（元/台）' },
        { label: '广告费用投入', unit: '（百万元）' },
        { label: '销售人员数量', unit: '（人）' },
        { label: '销售人员费用', unit: '（百万元）' },
        { label: '产品质量评价', unit: '（1--5）' },
        { label: '产品研究费用', unit: '（百万元）' },
        { label: '一般市场销售量', unit: '（台）' },
        { label: '一般市场销售额', unit: '（百万元）' },
        { label: '理论市场占有率', unit: '（%）' },
        { label: '实际市场占有率', unit: '（%）' },
        { label: '附加市场I销售量', unit: '（台）' },
        { label: '附加市场I销售额', unit: '（百万元）' },
        { label: '附加市场II销售量', unit: '（台）' },
        { label: '附加市场II销售额', unit: '（百万元）' },
        { label: '中标企业', unit: '（打***号企业）' },
        { label: '中标企业投标价格', unit: '（台/元）' },
        { label: '原材料库存量', unit: '（台）' },
        { label: '附件库存量', unit: '（台）' },
        { label: '产品积累库存数量', unit: '（台）' },
        { label: '机器人数量', unit: '（个）' },
        { label: '研究人员数', unit: '（个）' },
        { label: '一般市场计划量', unit: '（台）' },
        { label: '一般市场生产量', unit: '（台）' },
        { label: '维修保养系数', unit: '（0--1）' },
        { label: '合理化系数', unit: '（0--1）' },
        { label: '生产线生产能力', unit: '（台/周期）' },
        { label: '生产人员数', unit: '（个）' },
        { label: '生产线负载率', unit: '（%）' },
        { label: '生产人员负载率', unit: '（%）' },
        { label: '一般市场的产品成本', unit: '（元）' },
        { label: '税前经营成果', unit: '（百万元）' },
        { label: '本周期亏损结转', unit: '（百万元）' },
        { label: '本周期股息支付', unit: '（百万元）' },
        { label: '本周期利润储备', unit: '（百万元）' },
        { label: '本周期中期贷款', unit: '（百万元）' },
        { label: '本周期期末现金', unit: '（百万元）' },
        { label: '总的利润储备额', unit: '（百万元）' },
        { label: '本周期透支贷款', unit: '（百万元）' },
        { label: '资产负债总和', unit: '（百万元）' },
      ]);

    const fetchReportData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/enterreporting/', {
            withCredentials: true
      });
        reportData.value = response.data['各企业市场营销及生产研究报告'];  
      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    const currentReportData = computed(() => {
      return reportData.value[`各企业市场营销及生产研究报告（第${selectedCycle.value}周期）`] || [];
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
      currentReportData,
      reportItems
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
      margin-left: auto;
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
  