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
              <tr>
                <td>一般市场价格</td>
                <td>0</td>
                <td>实际市场占有</td>
                <td>1</td>
                <td>税前企业盈利</td>
                <td>0</td>
              </tr>
              <tr>
                <td>广告费用投入</td>
                <td>0</td>
                <td>一般市场产量</td>
                <td>0</td>
                <td>周期缴纳税收</td>
                <td>3</td>
              </tr>
              <tr>
                <td>销售人员数量</td>
                <td>0</td>
                <td>累积产品库存</td>
                <td>0</td>
                <td>机器人累计数</td>
                <td>3</td>
              </tr>
              <tr>
                <td>一般市场计划</td>
                <td>0</td>
                <td>生产人员数量</td>
                <td>0</td>
                <td>设备生产能力</td>
                <td>0</td>
              </tr>
              <tr>
                <td>一般市场销量</td>
                <td>0</td>
                <td>生产设备负荷</td>
                <td>5</td>
                <td>总的盈亏累计</td>
                <td>56</td>
              </tr>
              <tr>
                <td>研发投入效应</td>
                <td>0</td>
                <td>生产人员负荷</td>
                <td>5</td>
                <td>周期贷款总额</td>
                <td>10</td>
              </tr>
              <tr>
                <td>一般市场销额</td>
                <td>0</td>
                <td>周期支付股息</td>
                <td>10</td>
                <td>周期期末现金</td>
                <td>0</td>
              </tr>
              <tr>
                <td>理论市场占有</td>
                <td>1</td>
                <td>产品质量评价</td>
                <td>2</td>
                <td>资产负债合计</td>
                <td>4</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { useUserStore } from '@/store/user';


export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;

    return {
      userInfo,
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
