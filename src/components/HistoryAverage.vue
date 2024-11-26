<template>
    <div class="panel panel-default mt-3">
      <div class="panel-heading">
        <h3 class="panel-title">历史平均材料价格、工资水平及创业注册资金数据</h3>
      </div>
      <div class="panel-body">
          <div class="table-container">
            <div class="header">材料价格</div>
            <table>
              <thead>
                <tr>
                  <th rowspan="2">订购批量</th>
                  <th colspan="2">单位价格（元）</th>
                </tr>
                <tr>
                  <th>原材料</th>
                  <th>附件</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(batch, index) in Data.materials.batches" :key="index">
                  <td>{{ batch }}</td>
                  <td>{{ Data.materials.rawPrices[index] }}</td>
                  <td>{{ Data.materials.accessoryPrices[index] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">工资水平</div>
            <table>
              <thead>
                <tr>
                  <th>部门</th>
                  <th>年薪（万元）</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(dept, index) in Data.salaries.departments" :key="index">
                  <td>{{ dept }}</td>
                  <td>{{ Data.salaries.amounts[index] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="table-container">
            <div class="header">初始资金</div>
            <table>
              <thead>
                <tr>
                  <th>资金类型</th>
                  <th>数额（万元）</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(type, index) in Data.funds.types" :key="index">
                  <td>{{ type }}</td>
                  <td>{{ Data.funds.amounts[index] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
      </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const Data = ref({
      materials: { batches: [], rawPrices: [], accessoryPrices: [] },
      salaries: { departments: [], amounts: [] },
      funds: { types: [], amounts: [] }
    });

    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/lookhistory/', {
          withCredentials: true
        });
        
        const data = response.data;
        
        // 填充材料价格
        Data.value.materials.batches = data['订购批量_批量范围'];
        Data.value.materials.rawPrices = data['订购批量_原材料单价（元）'];
        Data.value.materials.accessoryPrices = data['订购批量_附件单价（元）'];

        // 填充工资水平
        Data.value.salaries.departments = data['部门'];
        Data.value.salaries.amounts = data['年薪（万元）'];

        // 填充初始资金
        Data.value.funds.types = data['资金类型'];
        Data.value.funds.amounts = data['数额（万元）'];

      } catch (error) {
        console.error('获取报告数据时出错:', error);
      }
    };  

    onMounted(() => {
      fetchData();
    });

    return {
      Data
    };
  },
};
</script>

<style scoped>
.panel {
  margin-top: 20px;
  border-radius: 8px;
}

.panel-heading {
  background-color: #f7f7f9;
  padding: 15px;
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
