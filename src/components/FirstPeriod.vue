<template>
  <div class="panel panel-default mt-3">
    <div class="panel-heading">
      <h3 class="panel-title">第 1 周期（创业周期）市场形势报告</h3>
    </div>
    <div class="panel-body">
      <table class="table table-striped">
        <tbody>
          <tr v-for="(value, key) in reportData" :key="key">
            <td class="highlight">{{ key }}</td>
            <td>{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const reportData = ref({});

const fetchReportData = async () => {
  try {

    const response = await axios.get('http://127.0.0.1:8000/users/look1/', {
            withCredentials: true
  });
    const data = response.data;

    const reportTitle = '第1周期（创业周期）市场形势报告';

    // 直接获取第 1 周期市场形势报告的内容
    if (data[reportTitle]) {
      // 这部分可以根据后台返回的数据结构做相应调整
      reportData.value = {
        '市场容量': data[reportTitle]['市场容量'] || '无相关数据',
        '原材料': data[reportTitle]['原材料'] || '无相关数据',
        '附件': data[reportTitle]['附件'] || '无相关数据',
        '人员费用': data[reportTitle]['人员费用'] || '无相关数据',
        '批量招标': data[reportTitle]['批量招标'] || '无相关数据',
        '批量订购': data[reportTitle]['批量订购'] || '无相关数据',
        '订购价格': data[reportTitle]['订购价格'] || '无相关数据',
      };
    } else {
      reportData.value = { '内容': '无相关数据' };
    }
  } catch (error) {
    console.error('请求出错:', error);
    reportData.value = { '错误': '无法获取数据' };
  }
};

onMounted(() => {
  fetchReportData();
});
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

.table-striped > tbody > tr:nth-child(odd) {
  background-color: #f9f9f9;
  border-radius: 5px;
}

.highlight {
    background-color: #f3776c;
    color: #fff;
}
</style>
