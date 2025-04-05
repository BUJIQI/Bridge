<template>
  <div>
    <div class="no-report-message" v-if="userInfo.cycle === 8">本轮七周决策已全部结束<br>可前往查看全部结果</div>
    <div v-else>
      <div class="panel panel-default mt-3">
        <div class="panel-heading">
          <h3 class="panel-title">
            第{{ userInfo?.cycle }}周期决策数据输入
            <el-tooltip placement="right">
              <template #content>点击决策项目名称，<br />如“一般市场价格”，<br />获取名词解释信息。</template>
              <Warning class="warning-icon" />
            </el-tooltip>
          </h3>
          <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="offcanvas" data-bs-target="#aiReportOffcanvas" aria-controls="aiReportOffcanvas">
            AI辅助决策
          </button>
        </div>
        <div class="panel-body">
          <section class="decision-section sales">
            <h2>销售</h2>
            <div class="input-group" v-for="(value, key) in salesFields" :key="key">
              <label :for="value" @click="showExplanation(key)">{{ key }}</label>
              <div class="input-wrapper" :id="value">
                <select v-if="key === '市场和生产研究报告'" :id="value" v-model="formData[value]">
                  <option value="Y">Y</option>
                  <option value="N">N</option>
                </select>
                <input v-else type="text" :id="value" v-model="formData[value]" />
                <span class="unit">{{ units[value] }}</span>
              </div>
            </div>
          </section>

          <section class="decision-section production">
            <h2>生产</h2>
            <div class="input-group" v-for="(value, key) in productionFields" :key="key">
              <label :for="value" @click="showExplanation(key)">{{ key }}</label>
              <div class="input-wrapper" :id="value">
                <input type="text" :id="value" v-model="formData[value]" />
                <span class="unit">{{ units[value] }}</span>
              </div>
            </div>
          </section>

          <section class="decision-section purchasing">
            <h2>采购</h2>
            <div class="input-group" v-for="(value, key) in purchasingFields" :key="key">
              <label :for="value" @click="showExplanation(key)">{{ key }}</label>
              <div class="input-wrapper" :id="value">
                <input type="text" :id="value" v-model="formData[value]" />
                <span class="unit">{{ units[value] }}</span>
              </div>
            </div>
          </section>

          <section class="decision-section quality">
            <h2>质量</h2>
            <div class="input-group" v-for="(value, key) in qualityFields" :key="key">
              <label :for="value" @click="showExplanation(key)">{{ key }}</label>
              <div class="input-wrapper" :id="value">
                <input type="text" :id="value" v-model="formData[value]" />
                <span class="unit">{{ units[value] }}</span>
              </div>
            </div>
          </section>

          <section class="decision-section finance">
            <h2>财务</h2>
            <div class="input-group" v-for="(value, key) in financeFields" :key="key">
              <label :for="value" @click="showExplanation(key)">{{ key }}</label>
              <div class="input-wrapper" :id="value">
                <input type="text" :id="value" v-model="formData[value]" />
                <span class="unit">{{ units[value] }}</span>
              </div>
            </div>
          </section>
          <div class="custom-button">
            <button class="decision-button" @click="submitDecision">
              提交决策
            </button>
          </div>
        </div>
      </div>
    </div>
    <transition name="fade" v-for="(isVisible, key) in explanationVisibility" :key="key" appear>
        <div v-if="isVisible" :style="explanationStyle[key]" class="explanation-box">
          {{ explanations[key] }}
          <div class="details-container">
            <span class="arrow" @click="navigateToNounsExplanation(key)"></span>
            <span class="details" @click="navigateToNounsExplanation(key)">查看详情</span>
          </div>
        </div>
    </transition>

    <!-- AI辅助决策结果 Offcanvas -->
    <div class="offcanvas offcanvas-start" style="width: 350px;" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="aiReportOffcanvas" aria-labelledby="aiReportOffcanvasLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="aiReportOffcanvasLabel">AI辅助决策</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body v-html-content">
        <pre v-if="aiResult" v-html="aiResult"></pre>
        <button class="btn btn-primary mt-3" @click="generateDecision">生成决策</button>
      </div>
    </div>   
  </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import { ref, computed, watch, onMounted } from 'vue';
import axios from '@/api/axios';
import Swal from 'sweetalert2';
import { useRouter } from 'vue-router';
import { marked } from 'marked';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;
    const explanations = ref({});
    const explanationVisibility = ref({});
    const explanationStyle = ref({});
    const explanationTimer = ref({});
    const currentLabel = ref('');
    const router = useRouter(); 
    const aiResult = ref('');

    // 定义初始输入数据
    const formData = ref({
      general_market_price: '1150',
      advertising_investment: '1',
      sales_staff: '40',
      market_research_report: 'N',
      bid_price: '0',
      special_product_qty: '2000',
      production_plan_qty: '21600',
      production_line_investment: '0',
      production_line_change: '0',
      maintenance_cost: '0.1',
      production_optimization_investment: '0',
      production_staff_recruitment: '4',
      production_staff_resignation: '0',
      purchase_robot: '0',
      raw_material_purchase_qty: '21600',
      purchase_accessories: '20800',
      research_staff_recruitment: '0',
      research_staff_resignation: '0',
      product_improvement_cost: '0.39',
      social_benefits: '80',
      medium_term_loan: '5',
      purchase_securities: '0',
      planned_dividend_payment: '0.3',
      management_optimization_investment: '0'
    });

    // 定义字段和单位
    const salesFields = {
      '一般市场价格': 'general_market_price',
      '广告费用投入': 'advertising_investment',
      '销售人员个数': 'sales_staff',
      '市场和生产研究报告': 'market_research_report',
      '附一：投标价格': 'bid_price',
      '附二：特殊产品数': 'special_product_qty'
    };

    const productionFields = {
      '一般市场产品计划量': 'production_plan_qty',
      '生产线投资数': 'production_line_investment',
      '生产线变卖数': 'production_line_change',
      '维修保养费用': 'maintenance_cost',
      '生产合理化投资': 'production_optimization_investment',
      '生产人员招收数': 'production_staff_recruitment',
      '生产人员辞退数': 'production_staff_resignation',
      '购买机器人': 'purchase_robot'
    };

    const purchasingFields = {
      '购买原材料量': 'raw_material_purchase_qty',
      '购买附件量': 'purchase_accessories'
    };

    const qualityFields = {
      '科研人员招收数': 'research_staff_recruitment',
      '科研人员辞退数': 'research_staff_resignation',
      '产品改进费用': 'product_improvement_cost'
    };

    const financeFields = {
      '社会福利费用': 'social_benefits',
      '中期贷款': 'medium_term_loan',
      '购买有价证券': 'purchase_securities',
      '计划支付股息': 'planned_dividend_payment',
      '管理合理化投资': 'management_optimization_investment'
    };

    const units = {
      general_market_price: '元/台',
      advertising_investment: '百万元',
      sales_staff: '个',
      market_research_report: 'Y/N',
      bid_price: '元/台',
      special_product_qty: '台',
      production_plan_qty: '台',
      production_line_investment: '条',
      production_line_change: '条',
      maintenance_cost: '百万元',
      production_optimization_investment: '百万元',
      production_staff_recruitment: '个',
      production_staff_resignation: '个',
      purchase_robot: '个',
      raw_material_purchase_qty: '单位',
      purchase_accessories: '单位',
      research_staff_recruitment: '个',
      research_staff_resignation: '个',
      product_improvement_cost: '百万元',
      social_benefits: '%',
      medium_term_loan: '百万元',
      purchase_securities: '百万元',
      planned_dividend_payment: '百万元',
      management_optimization_investment: '百万元'
    };

    // 计算属性对象，根据 userInfo?.cycle 设置多个字段的值
    const dynamicFields = computed({
      get() {
        return {
          production_line_investment: userInfo?.cycle === 1 ? 2 : 0,
          production_staff_recruitment: userInfo?.cycle === 1 ? 30 : 4,
          research_staff_recruitment: userInfo?.cycle === 1 ? 2 : 0
        };
      },
      set(values) {
        formData.value.production_line_investment = values.production_line_investment;
        formData.value.production_staff_recruitment = values.production_staff_recruitment;
        formData.value.research_staff_recruitment = values.research_staff_recruitment;
      }
    });

    // 监听 dynamicFields 并更新 formData
    watch(dynamicFields, (newValues) => {
      formData.value.production_line_investment = newValues.production_line_investment;
      formData.value.production_staff_recruitment = newValues.production_staff_recruitment;
      formData.value.research_staff_recruitment = newValues.research_staff_recruitment;
    }, { immediate: true });

    // 键名映射对象
    const keyMapping = {
      '附一：投标价格': '附加市场I--投标价格',
      '附二：特殊产品数': '附加市场II--特殊产品数',
      '购买原材料量': '购买原材料、附件量',
      '购买附件量': '购买原材料、附件量',
      '科研人员招收数': '研发人员招收和辞退',
      '科研人员辞退数': '研发人员招收和辞退',
    };    

    const showExplanation = async (label) => {
      // 隐藏所有解释框
      for (const key in explanationVisibility.value) {
        explanationVisibility.value[key] = false;
      }

      currentLabel.value = label;
      try {
        const response = await axios.get(`/users/decision_terms_introduction/`, {
          withCredentials: true
        });
        const data = response.data;
        explanations.value[label] = data[keyMapping[label] || label];

        // 找到对应的 input-wrapper 元素
        const inputWrapper = document.getElementById(salesFields[label] || productionFields[label] || purchasingFields[label] || qualityFields[label] || financeFields[label]);
        if (inputWrapper) {
          const rect = inputWrapper.getBoundingClientRect();
          explanationStyle.value[label] = {
            top: `${rect.bottom + window.scrollY - 35}px`,
            left: `${rect.right + window.scrollX + 40}px`
          };
        }

        // 显示解释框
        explanationVisibility.value[label] = true;

        // 设置定时器隐藏解释框
        if (explanationTimer.value[label]) {
          clearTimeout(explanationTimer.value[label]);
        }
        explanationTimer.value[label] = setTimeout(() => {
          explanationVisibility.value[label] = false;
        }, 30000);
      } catch (error) {
        console.error('获取名词解释时发生错误:', error);
        Swal.fire('错误', '获取名词解释时发生错误，请重试。', 'error');
      }
    };

    const navigateToNounsExplanation = (label) => {
      if (label) {
        router.push({ name: 'NounsExplanation', params: { noun: label } });
      }
    };

    const generateDecision = async () => {
      try {
        Swal.fire({
          title: 'AI分析结果正在生成中...',
          allowOutsideClick: false,
          showConfirmButton: false,
          width: '400px',
          didOpen: () => {
            Swal.showLoading();
          }
        });

        const response = await axios.get('/users/AIaided_decision_making/', {
          withCredentials: true
        });
        const data = response.data;
        // 使用marked将Markdown转换为HTML
        aiResult.value = marked(data.decision);

        // 关闭SweetAlert2弹窗
        Swal.close();

        // 保存到localStorage，使用用户ID作为键的一部分
        const userId = userInfo.stuid; 
        localStorage.setItem(`aiResult_${userId}`, aiResult.value);
      } catch (error) {
        console.error('请求AI辅助决策时发生错误:', error);
        Swal.fire('错误', '请求AI辅助决策时发生错误，请重试。', 'error');
      }
    };

    const loadAiResultFromStorage = () => {
      const userId = userInfo.stuid;
      const storedAiResult = localStorage.getItem(`aiResult_${userId}`);
      if (storedAiResult) {
        aiResult.value = storedAiResult;
      }
    };

    const submitDecision = async () => {
      const result = await Swal.fire({
        title: '确认提交',
        text: '您确定要提交决策数据吗？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      });

      if (result.isConfirmed) {
        Swal.fire({
          title: '正在提交决策数据，请稍候...',
          allowOutsideClick: false,
          showConfirmButton: false,
          didOpen: () => {
            Swal.showLoading();
          }
        });
        try {
          const response = await axios.post('/users/commit_decision/', formData.value, {
            withCredentials: true
          });
          const submitResult = response.data;
          Swal.close();

          if (submitResult['提交结果'] === '决策数据已经成功递交') {
            Swal.fire('成功', '决策数据已经成功递交，可前往查看竞争结果报表', 'success').then(() => {
              // 更新周期
              const userInfoString = localStorage.getItem('userInfo');
              const userInfoObject = JSON.parse(userInfoString);
              userInfoObject.cycle = submitResult['提交后周期'];
              localStorage.setItem('userInfo', JSON.stringify(userInfoObject));
               // 清空AI结果缓存
              const userId = userInfo.stuid;
              localStorage.removeItem(`aiResult_${userId}`); 
              window.location.reload(); // 自动刷新页面
            });
          } else {
            Swal.fire('失败', submitResult['提交结果'], 'error');
          }
        } catch (error) {
          console.error('提交决策时发生错误:', error);
          Swal.fire('错误', '提交决策时发生错误，请重试。', 'error');
        }
      } else {
        Swal.fire('已取消', '您的决策数据未提交', 'info');
      }
    };

    // 组件挂载时加载AI结果
    onMounted(() => {
      loadAiResultFromStorage();
    });

    return {
      userInfo,
      formData,
      dynamicFields,
      salesFields,
      productionFields,
      purchasingFields,
      qualityFields,
      financeFields,
      units,
      explanations,
      explanationVisibility,
      explanationStyle,
      explanationTimer,
      showExplanation,
      navigateToNounsExplanation,
      generateDecision,
      aiResult,
      submitDecision
    };
  },
}
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

.warning-icon {
  width: 20px;
  height: 20px;
  color: #888888;
}

.btn-danger {
    background-color: rgb(255, 82, 82);
    border: none;
    font-size: 16px;
    padding: 8px;
}

.btn-danger:hover {
    background-color: rgb(207, 61, 61);
    color: #ffffff;
}

.offcanvas-body pre {
  white-space: pre-wrap;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 5px;
  border: 1px solid #ddd;
  max-height: 80vh;
  overflow-y: auto;
  font-family: Arial, sans-serif;
  color: #333;
  line-height: 1.5;
  margin: 0;
}

.btn-primary {
  background-color: #ec7676;
  border: none;
  font-size: 16px;
  padding: 8px;
  margin-bottom: 20px;
}

.btn-primary:hover {
  background-color: #c96060;
}

:deep(.v-html-content h3) {
  margin: 0;
  padding: 0 0 0 10px;
}

:deep(.v-html-content p) {
  margin: 0;
  padding: 0 0 0 10px;
}

:deep(.v-html-content ol) {
  margin: 0;
  padding: 0 0 0 10px;
}

:deep(.v-html-content ul) {
  margin: 0;
  padding: 0 0 0 10px;
}

:deep(.v-html-content li) {
  margin: 0;
  padding: 0 0 0 10px;
}

.panel-body {
  background-color: #ebdcdc;
  padding: 20px;
  border-radius: 8px;
}

.decision-section {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 20px;
}

.decision-section h2 {
  color: #333;
  border-bottom: 2px solid #e53935;
  padding-bottom: 5px;
}

.input-group {
  display: flex;
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  color: #666;
  margin-bottom: 5px;
  margin-top: 5px;
  width: 170px;
  cursor: pointer; 
  transition: color 0.3s, font-weight 0.3s; 
}

.input-group label:hover {
  color: #333;
  font-weight: bold; 
}

.input-wrapper {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.input-wrapper input,
.input-wrapper select {
  flex: 1;
  padding: 5px;
  border: 1px solid #888;
  border-radius: 4px;
  margin-right: 5px;
  width: 200px;
}

.input-wrapper .unit {
  color: #666;
  font-size: 0.9em;
}

.custom-button {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.decision-button {
  background-color: #e74c3c; 
  color: white;     
  padding: 10px; 
  width: 150px;                  
  border-radius: 5px;  
  border: none;      
  cursor: pointer;             
  transition: background-color 0.3s, transform 0.2s; 
}

.decision-button:hover {
  background-color: #c0392b;  
  transform: scale(1.05);      
}

.decision-button:active {
  transform: scale(0.95);     
}

.explanation-box {
  position: absolute;
  background-color: #fff;
  border: 1px solid #ea8787;
  font-size: 14px;
  color: #3d3b3b;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-width: 400px;
}

.details-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.arrow {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-bottom: 1px solid #666; 
  border-right: 1px solid #666; 
  transform: rotate(-45deg);
  transition: transform 0.3s ease, border-color 0.3s ease;
  margin-right: 4px; 
  cursor: pointer;
}

.details {
  color: #666;
  cursor: pointer;
  transition: color 0.3s ease;
  font-size: 12px;
}

.details-container:hover .arrow {
  border-bottom: 1px solid #444; 
  border-right: 1px solid #444; 
}

.details-container:hover .details {
  color: #444;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>