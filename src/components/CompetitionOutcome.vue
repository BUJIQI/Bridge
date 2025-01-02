<template>
  <div class="no-report-message" v-if="userInfo.cycle <= 1">尚未进行过决策，无结果可查看</div>
  <div v-else>  
    <div class="panel panel-default mt-3" v-if="userInfo.cycle > 1">
      <div class="panel-heading">
        <h3 class="panel-title">各企业主要竞争结果数据表（第{{ userInfo?.cycle-1 }}周期）</h3>
      </div>
      <div class="panel-body">
        <table class="data-table">
          <thead>
            <tr>
              <th colspan="2">项目/企业</th>
              <th>1</th>
              <th>2</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(values, key) in filteredCompeteOutcome" :key="key">
              <td>{{ key }}</td>
              <td>{{ presetValues[key] }}</td> 
              <td>{{ values[0] }}</td>
              <td>{{ values[1] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import axios from 'axios';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo

    return {
      userInfo,
    };
  
  },
  data() {
    return {
      competeOutcome: {},
      presetValues: {
        "一般市场价格": "元/台",
        "广告费用投入": "百万元",
        "销售人员数量": "人",
        "产品质量评价": "(1--5)",
        "一般市场销售量": "台",
        "一般市场销售额": "百万元",
        "理论市场占有率": "%",
        "实际市场占有率": "%",
        "附加市场I销售量": "台",
        "附加市场I销售额": "百万元",
        "附加市场II销售量": "台",
        "附加市场II销售额": "百万元",
        "中标企业": "打***号企业",
        "中标企业投标价格": "台/元",
        "产品累积库存数量": "台",
        "生产线生产能力": "台/周期",
        "税前经营成果": "百万元",
        "资产负债总和": "百万元"
      },
    firstElementValue: ''
    };
  },
  computed: {
    filteredCompeteOutcome() {
      return Object.fromEntries(Object.entries(this.competeOutcome).slice(1));
    }
  },
  created() {
    axios.get('http://127.0.0.1:8000/users/compete_outcome/', {
      withCredentials: true
      })
      .then(response => {
        this.competeOutcome = response.data;       
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
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
}

.panel-body {
  background-color: #ebdcdc;
  padding: 20px;
  border-radius: 8px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.data-table th {
  background-color: #c0392b; 
  color: #fff; 
}

.data-table tr:nth-child(even) {
  background-color: #e0e0e0; 
}

.data-table tr:hover {
  background-color: #ddd; 
}

.data-table td {
  color: #555;
}
</style>
