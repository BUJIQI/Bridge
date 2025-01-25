<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，不得显示评价总表</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">人机对抗评价指标权重</h3>
      </div>

      <div class="panel-body">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th colspan="2">市场类指标</th>
                <th colspan="2">生产类指标</th>
                <th colspan="2">财务类指标</th>
              </tr>
            </thead>
            <tbody>               
              <tr v-for="(item, index) in categorizedWeightData" :key="index">
                <template v-for="(subItem, subIndex) in item" :key="subIndex">
                  <td>{{ subItem.label || '' }}</td>
                  <td>{{ subItem.value !== undefined ? subItem.value : '' }}</td>
                </template>
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
    const WeightData = ref([]);

    const fetchReportData = async () => {
      try {
        const response = await axios.get('/users/summart_evaluation/', {
          withCredentials: true
        });
        
        WeightData.value = response.data['评价指标权重'];

      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };

    onMounted(() => {
      fetchReportData();
    });

    const categorizedWeightData = computed(() => {
      return [
        [
          { label: '一般市场价格', value: WeightData.value[0] },
          { label: '一般市场产量', value: WeightData.value[4] },
          { label: '税前企业盈利', value: WeightData.value[2] },
        ],
        [
          { label: '广告费用投入', value: WeightData.value[3] },
          { label: '累计产品库存', value: WeightData.value[7] },
          { label: '周期缴纳税收', value: WeightData.value[5] },
        ],
        [
          { label: '销售人员数量', value: WeightData.value[6] },
          { label: '生产人员数量', value: WeightData.value[10] },
          { label: '周期支付股息', value: WeightData.value[19] },
        ],
        [
          { label: '研发投入效应', value: WeightData.value[15] },
          { label: '生产设备负荷', value: WeightData.value[13] },
          { label: '总的盈亏累计', value: WeightData.value[14] },
        ],
        [
          { label: '一般市场计划', value: WeightData.value[9] },
          { label: '生产人员负荷', value: WeightData.value[16] },
          { label: '周期贷款总额', value: WeightData.value[17] },
        ],
        [
          { label: '一般市场销量', value: WeightData.value[12] },
          { label: '机器人累计数', value: WeightData.value[8] },
          { label: '周期期末现金', value: WeightData.value[20] },
        ],
        [
          { label: '一般市场销额', value: WeightData.value[18] },
          { label: '产品质量评价', value: WeightData.value[22] },
          { label: '资产负债合计', value: WeightData.value[23] },
        ],
        [
          { label: '理论市场占有', value: WeightData.value[21] },
          { label: '设备生产能力', value: WeightData.value[11] },
          { label: '', value: undefined }, // 占位符
        ],
        [
          { label: '实际市场占有', value: WeightData.value[1] },
          { label: '', value: undefined }, // 占位符
          { label: '', value: undefined }, // 占位符
        ],
      ];
    });

    return {
      userInfo,
      categorizedWeightData
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