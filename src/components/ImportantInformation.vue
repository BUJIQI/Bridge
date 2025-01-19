<template>
  <div class="row h-100">
    <div class="col-md-3 sidebar bg-light">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link
                class="list-link"
                :class="{ active: $route.path === '/important/rule' }"
                to="/important/rule"
              >
                决策基本规则
              </router-link>
            </li>
            <li class="nav-item">
              <a 
                href="#" 
                class="list-link" 
                @click="toggleMenu('explanation')"
                :class="{ collapsed: !subMenuVisible.explanation }"
              >
                决策名词解释
              <span class="arrow" :class="{ 'arrow-up': subMenuVisible.explanation, 'arrow-down': !subMenuVisible.explanation }"></span>
              </a>
              <ul v-if="subMenuVisible.explanation" class="submenu">
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('sales')"  
                    :class="{ collapsed: !subMenuVisible.sales }"
                  >            
                    销售
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.sales, 'arrow-down': !subMenuVisible.sales }"></span>
                  </a>
                  <ul v-if="subMenuVisible.sales" class="submenu">
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '一般市场价格') }" :to="{ name: 'NounsExplanation', params: { noun: '一般市场价格' } }">一般市场价格</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '广告费用投入') }" :to="{ name: 'NounsExplanation', params: { noun: '广告费用投入' } }">广告费用投入</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '销售人员个数') }" :to="{ name: 'NounsExplanation', params: { noun: '销售人员个数' } }">销售人员个数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '市场和生产研究报告') }" :to="{ name: 'NounsExplanation', params: { noun: '市场和生产研究报告' } }">市场和生产研究报告</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '附一：投标价格') }" :to="{ name: 'NounsExplanation', params: { noun: '附一：投标价格' } }">附一：投标价格</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '附二：特殊产品数') }" :to="{ name: 'NounsExplanation', params: { noun: '附二：特殊产品数' } }">附二：特殊产品数</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('production')"
                    :class="{ collapsed: !subMenuVisible.production }"
                  >
                    生产
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.production, 'arrow-down': !subMenuVisible.production }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.production" class="submenu">
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '一般市场产品计划量') }" :to="{ name: 'NounsExplanation', params: { noun: '一般市场产品计划量' } }">一般市场产品计划量</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '生产线投资数') }" :to="{ name: 'NounsExplanation', params: { noun: '生产线投资数' } }">生产线投资数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '生产线变卖数') }" :to="{ name: 'NounsExplanation', params: { noun: '生产线变卖数' } }">生产线变卖数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '维修保养费用') }" :to="{ name: 'NounsExplanation', params: { noun: '维修保养费用' } }">维修保养费用</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '生产合理化投资') }" :to="{ name: 'NounsExplanation', params: { noun: '生产合理化投资' } }">生产合理化投资</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '生产人员招收数') }" :to="{ name: 'NounsExplanation', params: { noun: '生产人员招收数' } }">生产人员招收数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '生产人员辞退数') }" :to="{ name: 'NounsExplanation', params: { noun: '生产人员辞退数' } }">生产人员辞退数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '购买机器人') }" :to="{ name: 'NounsExplanation', params: { noun: '购买机器人' } }">购买机器人</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('purchasing')"
                    :class="{ collapsed: !subMenuVisible.purchasing }"
                  >
                    采购
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.purchasing, 'arrow-down': !subMenuVisible.purchasing }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.purchasing" class="submenu">
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '购买原材料量') }" :to="{ name: 'NounsExplanation', params: { noun: '购买原材料量' } }">购买原材料量</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '购买附件量') }" :to="{ name: 'NounsExplanation', params: { noun: '购买附件量' } }">购买附件量</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('quality')"
                    :class="{ collapsed: !subMenuVisible.quality }"
                  >
                    质量
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.quality, 'arrow-down': !subMenuVisible.quality }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.quality" class="submenu">
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '科研人员招收数') }" :to="{ name: 'NounsExplanation', params: { noun: '科研人员招收数' } }">科研人员招收数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '科研人员辞退数') }" :to="{ name: 'NounsExplanation', params: { noun: '科研人员辞退数' } }">科研人员辞退数</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '产品改进费用') }" :to="{ name: 'NounsExplanation', params: { noun: '产品改进费用' } }">产品改进费用</router-link></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a 
                    href="#" 
                    class="list-link" 
                    @click="toggleMenu('finance')"
                    :class="{ collapsed: !subMenuVisible.finance }"
                  >
                    财务
                  <span class="arrow" :class="{ 'arrow-up': subMenuVisible.finance, 'arrow-down': !subMenuVisible.finance }"></span>
                  </a>                  
                  <ul v-if="subMenuVisible.finance" class="submenu">
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '社会福利费用') }" :to="{ name: 'NounsExplanation', params: { noun: '社会福利费用' } }">社会福利费用</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '中期贷款') }" :to="{ name: 'NounsExplanation', params: { noun: '中期贷款' } }">中期贷款</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '购买有价证券') }" :to="{ name: 'NounsExplanation', params: { noun: '购买有价证券' } }">购买有价证券</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '计划支付股息') }" :to="{ name: 'NounsExplanation', params: { noun: '计划支付股息' } }">计划支付股息</router-link></li>
                    <li class="nav-item"><router-link class="list-link" :class="{ active: isActive('NounsExplanation', '管理合理化投资') }" :to="{ name: 'NounsExplanation', params: { noun: '管理合理化投资' } }">管理合理化投资</router-link></li>
                  </ul>
                </li>
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
import { reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const subMenuVisible = reactive({
      explanation: false,
      sales: false,
      production: false,
      purchasing: false,
      quality: false,
      finance: false,
    });

    const activeMenu = reactive({
      explanation: false,
      sales: false,
      production: false,
      purchasing: false,
      quality: false,
      finance: false,
    });

    const toggleMenu = (menu) => {
      subMenuVisible[menu] = !subMenuVisible[menu];
    };

    const isActive = (name, noun) => {
      return route.name === name && route.params.noun === noun;
    };

    watch(
      () => route.path,
      (newPath) => {

        // 根据当前路径设置子菜单的激活状态
        if (newPath.includes('/important/nouns/')) {
          subMenuVisible.explanation = true;

          const noun = route.params.noun;
          if (noun) {
            if (['一般市场价格', '广告费用投入', '销售人员个数', '市场和生产研究报告', '附一：投标价格', '附二：特殊产品数'].includes(noun)) {
              subMenuVisible.sales = true;
            } else if (['一般市场产品计划量', '生产线投资数', '生产线变卖数', '维修保养费用', '生产合理化投资', '生产人员招收数', '生产人员辞退数', '购买机器人'].includes(noun)) {
              subMenuVisible.production = true;
            } else if (['购买原材料量', '购买附件量'].includes(noun)) {
              subMenuVisible.purchasing = true;
            } else if (['科研人员招收数', '科研人员辞退数', '产品改进费用'].includes(noun)) {
              subMenuVisible.quality = true;
            } else if (['社会福利费用', '中期贷款', '购买有价证券', '计划支付股息', '管理合理化投资'].includes(noun)) {
              subMenuVisible.finance = true;
            }
          }
        }
      },
      { immediate: true }
    );

    return {
      subMenuVisible,
      activeMenu,
      toggleMenu,
      isActive,
    };
  },
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

.list-link.active {
  background-color: #e0e0e0;
  color: #000000;
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