<template>
  <div class="row h-100">
    <div class="col-md-3 sidebar bg-light">
          <ul class="nav flex-column">
            <li class="nav-item">
              <a 
                href="#" 
                class="list-link" 
                @click="toggleMenu('makeDecision')"
                :class="{ collapsed: !subMenuVisible.makeDecision }"
              >
                进行决策
              <span class="arrow" :class="{ 'arrow-up': subMenuVisible.makeDecision, 'arrow-down': !subMenuVisible.makeDecision }"></span>
              </a>
              <ul v-if="subMenuVisible.makeDecision" class="submenu">
                <li class="nav-item"><router-link class="list-link" to="/decision/input">输入决策数据</router-link></li>                
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('budgetReports')"  
                    :class="{ collapsed: !subMenuVisible.budgetReports }"
                  >            
                    预算数据报告
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.budgetReports, 'arrow-down': !subMenuVisible.budgetReports }"></span>
                  </a>
                  <ul v-if="subMenuVisible.budgetReports" class="submenu">
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-market-production">市场生产数据报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-cost-type">成本类型核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-cost-department">成本发生部门报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-cost-unit">成本承担单元报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-profit-loss">利润亏损核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-after-tax-profit">税后利润核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-profit-distribution">利润分配核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-operating-financial">生产经营财务报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-balance-sheet">资产负债合计报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/budget-market-research">竞争市场调研报告</router-link></li>
                  </ul>                  
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('historyDecision')"
                    :class="{ collapsed: !subMenuVisible.historyDecision }"
                  >
                    历史决策
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.historyDecision, 'arrow-down': !subMenuVisible.historyDecision }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.historyDecision" class="submenu">
                    <li v-for="cycle in historyCyclesToDisplay" :key="cycle" class="nav-item">
                      <router-link class="list-link" :to="`/decision/history-decision/${cycle}`" @click="selectedHistory(cycle)">第{{ cycle }}周期</router-link>
                    </li>
                  </ul>
                </li>
              </ul>              
            </li>
            <li class="nav-item">
              <a 
                href="#" 
                class="list-link" 
                @click="toggleMenu('dataReports')"
                :class="{ collapsed: !subMenuVisible.dataReports }"
              >
                数据报表
              <span class="arrow" :class="{ 'arrow-up': subMenuVisible.dataReports, 'arrow-down': !subMenuVisible.dataReports }"></span>
              </a>
              <ul v-if="subMenuVisible.dataReports" class="submenu">
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('marketCycle')"  
                    :class="{ collapsed: !subMenuVisible.marketCycle }"
                  >            
                    市场周期形势
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.marketCycle, 'arrow-down': !subMenuVisible.marketCycle }"></span>
                  </a>
                  <ul v-if="subMenuVisible.marketCycle" class="submenu">
                    <li v-for="cycle in marketCyclesToDisplay" :key="cycle" class="nav-item">
                      <router-link class="list-link" :to="`/decision/cycle/${cycle}`" @click="selectedHistory(cycle)">第{{ cycle }}周期</router-link>
                    </li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/cycle/average">历史平均</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('companyData')"
                    :class="{ collapsed: !subMenuVisible.companyData }"
                  >
                    企业数据报表
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.companyData, 'arrow-down': !subMenuVisible.companyData }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.companyData" class="submenu">
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/market-production">市场生产数据报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/cost-type">成本类型核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/cost-department">成本发生部门报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/cost-unit">成本承担单元报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/profit-loss">利润亏损核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/after-tax-profit">税后利润核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/profit-distribution">利润分配核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/operating-financial">生产经营财务报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/balance-sheet">资产负债合计报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/decision/company/market-research">竞争市场调研报告</router-link></li>
                  </ul>
                </li>
              </ul>
            </li>

            <li class="nav-item"><router-link class="list-link" to="/decision/outcome">竞争结果报表</router-link></li>

            <li class="nav-item">
              <a 
                href="#" 
                class="list-link" 
                @click="toggleMenu('evaluation')"
                :class="{ collapsed: !subMenuVisible.evaluation }"
              >             
                决策评价总表
              <span class="arrow" :class="{ 'arrow-up': subMenuVisible.evaluation, 'arrow-down': !subMenuVisible.evaluation }"></span>
              </a>
              <ul v-if="subMenuVisible.evaluation" class="submenu">
                <li class="nav-item"><router-link class="list-link" to="/decision/evaluation/market">市场类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/decision/evaluation/production">生产类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/decision/evaluation/finance">财务类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/decision/evaluation/overall">决策综合评价</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/decision/evaluation/weight">评价指标权重</router-link></li>
              </ul>
            </li>
          </ul>
    </div>

    <div class="col-md-9">
      <router-view />
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/user';

export default {
  setup() {
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;
    const selectedHistory = (cycle) => {
            userStore.setSelectedHistory(cycle);
            localStorage.setItem('SelectedPeriod', cycle);
    };

    // 对于历史决策，只返回当前周期之前的周期
    const historyCyclesToDisplay = [];
    for (let i = 1; i < userInfo.cycle; i++) {
      historyCyclesToDisplay.push(i);
    }

    // 对于市场周期形势，返回当前周期及之前的周期
    const marketCyclesToDisplay = [];
    if (userInfo.cycle !== 8) {
      for (let i = 1; i <= userInfo.cycle; i++) {
        marketCyclesToDisplay.push(i);
      }
    } else {
      // 当 userInfo.cycle 等于 8 时展示 1-7 周期
      for (let i = 1; i <= 7; i++) {
        marketCyclesToDisplay.push(i);
      }
    }

    return {
      userInfo,
      selectedHistory,
      subMenuVisible: {
        makeDecision: false,
        budgetReports: false,
        dataReports: false,
        marketCycle: false,
        competitionResults: false,
        evaluation: false,
        companyData: false,
      },
      historyCyclesToDisplay,
      marketCyclesToDisplay,
    };
  },
  methods: {
    toggleMenu(menu) {
      this.subMenuVisible[menu] = !this.subMenuVisible[menu];
    },

  }
};
</script>

<style scoped>
.sidebar {
  padding: 40px;
}

.list-link {
  cursor: pointer;
  color: #333;
  transition: background-color 0.3s;
  display: flex;
  justify-content: space-between; 
  align-items: center;
  padding: 8px 15px;
  border-radius: 4px;
  text-decoration: none;
}

.list-link:hover {
  background-color: #f0f0f0;
}

.panel {
  margin-top: 20px;
  border-radius: 8px;
}

.panel-heading {
  background-color: #f7f7f9;
  padding: 15px;
  font-size: 1.25rem;
}

.panel-body {
  padding: 20px;
}

.table-striped > tbody > tr:nth-child(odd) {
  background-color: #f9f9f9;
  border-radius: 5px;
}

.arrow {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-bottom: 2px solid #333; 
  border-right: 2px solid #333; 
  transform: rotate(45deg);
  transition: transform 0.3s ease;
  margin-left: 8px; 
}

.arrow-up {
  transform: rotate(-135deg);
}

.arrow-down {
  transform: rotate(45deg);
}

.submenu {
  padding-left: 15px;
  list-style-type: none;
  border-left: 2px solid #ccc;
  margin-left: 10px; 
}

.nav-item {
    color: #ffffff;
}
</style>