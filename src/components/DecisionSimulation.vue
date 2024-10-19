<template>
  <div class="full">
    <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark" >
      <div class="container-fluid">
        <router-link class="navbar-brand" href="#">
          <img src="@/assets/info.gif" alt="ICEDSS" width="40" height="40">
          JCTD
        </router-link>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/welcome">决策仿真</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/important">重要信息</router-link>
            </li>
            <li class="nav-item">
              <button @click="reset" class="btn btn-danger" style="padding: 5px; margin: 5px; ">
                新的一轮
              </button>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <div class="info"  style="border: 1px solid #ccc; padding: 5px; margin: 5px; border-radius: 20px;">
                当前：
                第<span class="text-danger">{{ userInfo?.group }}</span>组 
                第<span class="text-danger">{{ userInfo?.number }}</span>企业 
                <span class="text-danger">{{ userInfo?.rival }}</span>位竞争对手 
                第<span class="text-danger">{{ userInfo?.cycle }}</span>周期          
              </div>
            </li>            
            <li class="nav-item">
              <router-link class="nav-link" to="/logout">注销</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">我的资料</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row h-100">
        <div class="col-md-3 sidebar bg-light">
          <ul class="nav flex-column">
            <li class="nav-item">
              <a href="#" class="list-link active">进行决策</a>
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
                    <li v-for="cycle in cyclesToDisplay" :key="cycle" class="nav-item">
                      <router-link class="list-link" :to="`/market/cycle/${cycle}`">第{{ cycle }}周期</router-link>
                    </li>
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
                    <li class="nav-item"><router-link class="list-link" to="/company/market-production">市场生产数据报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/cost-type">成本类型核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/cost-department">成本发生部门报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/cost-unit">成本承担单元报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/profit-loss">利润亏损核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/after-tax-profit">税后利润核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/profit-distribution">利润分配核算报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/operating-financial">生产经营财务报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/balance-sheet">资产负债合计报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" to="/company/market-research">竞争市场调研报告</router-link></li>
                  </ul>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <a href="#" class="list-link">竞争结果报表</a>
            </li>
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
                <li class="nav-item"><router-link class="list-link" to="/evaluation/market">市场类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/evaluation/production">生产类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/evaluation/finance">财务类指标</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/evaluation/overall">决策综合评价</router-link></li>
                <li class="nav-item"><router-link class="list-link" to="/evaluation/weight">评价指标权重</router-link></li>
              </ul>
            </li>
          </ul>
        </div>

        <div class="col-md-9">
          <router-view></router-view>
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


    let cyclesToDisplay = ['一', '二', '三', '四', '五', '六', '七'];
    const chineseToNumberMap = {
      '一': 1,
      '二': 2,
      '三': 3,
      '四': 4,
      '五': 5,
      '六': 6,
      '七': 7,
    };
    const cycleNumber = chineseToNumberMap[userInfo.cycle] || 0;
    if (cycleNumber) {
      cyclesToDisplay = cyclesToDisplay.slice(0, cycleNumber);
    }  

    return {
      userInfo,
      subMenuVisible: {
        dataReports: false,
        marketCycle: false,
        competitionResults: false,
        evaluation: false,
        companyData: false,
      },
      cyclesToDisplay,
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
.full {
  height: 100vh;
  width: 100vw;
}

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

.nav-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #3c3737;
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