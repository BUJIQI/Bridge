<template>
    <div class="panel panel-default mt-3">
        <div class="panel-heading">
            <h3 class="panel-title">{{ matchingKey }}</h3> 
        </div>
        <div class="panel-body">
            <section class="decision-section sales">
                <h2>销售</h2>
                <div class="input-group">
                    <label>一般市场价格</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.一般市场价格" disabled />
                        <span class="unit">元/台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>广告费用投入</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.广告费用投入" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>销售人员个数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.销售人员个数" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>市场和生产研究报告</label>
                    <div class="input-wrapper">
                        <select :value="historicalDecisionData[matchingKey]?.市场和生产研究报告" disabled>
                            <option value="Y">Y</option>
                            <option value="N">N</option>
                        </select>
                        <span class="unit">Y/N</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>附一：投标价格</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.['附一：投标价格']" disabled />
                        <span class="unit">元/台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>附二：特殊产品数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.['附二：特殊产品数']" disabled />
                        <span class="unit">台</span>
                    </div>
                </div>
            </section>

            <section class="decision-section production">
                <h2>生产</h2>
                <div class="input-group">
                    <label>一般市场产品计划量</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.一般市场产品计划量" disabled />
                        <span class="unit">台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产线投资数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.生产线投资数" disabled />
                        <span class="unit">条</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产线变卖数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.生产线变卖数" disabled />
                        <span class="unit">条</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>维修保养费用</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.维修保养费用" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产合理化投资</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.生产合理化投资" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产人员招收数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.生产人员招收数" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产人员辞退数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.生产人员辞退数" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买机器人</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.购买机器人" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>
            </section>

            <section class="decision-section purchasing">
                <h2>采购</h2>
                <div class="input-group">
                    <label>购买原材料量</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.购买原材料量" disabled />
                        <span class="unit">单位</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买附件量</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.购买附件量" disabled />
                        <span class="unit">单位</span>
                    </div>
                </div>
            </section>

            <section class="decision-section quality">
                <h2>质量</h2>
                <div class="input-group">
                    <label>科研人员招收数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.科研人员招收数" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>科研人员辞退数</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.科研人员辞退数" disabled />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>产品改进费用</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.产品改进费用" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>
            </section>

            <section class="decision-section finance">
                <h2>财务</h2>
                <div class="input-group">
                    <label>社会福利费用</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.社会福利费用" disabled />
                        <span class="unit">%</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>中期贷款</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.中期贷款" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买有价证券</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.购买有价证券" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>计划支付股息</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.计划支付股息" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>管理合理化投资</label>
                    <div class="input-wrapper">
                        <input type="text" :value="historicalDecisionData[matchingKey]?.管理合理化投资" disabled />
                        <span class="unit">百万元</span>
                    </div>
                </div>
            </section>
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
            userStore.setSelectedHistory(sessionStorage.getItem('SelectedPeriod'));
            
        const selectedHistory = computed(() => userStore.selectedHistory);  
        const historicalDecisionData = ref({}); 

        const fetchHistoricalDecision = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/users/historical_decision/', {
                    withCredentials: true
                });
                historicalDecisionData.value = response.data; 
            } catch (error) {
                console.error('获取历史决策数据时发生错误:', error);
            }
        };

        // 在组件挂载时请求数据
        onMounted(() => {
            fetchHistoricalDecision();
        });

        // 计算属性：检查是否存在 selectedHistory 字段对应的数据
        const matchingKey = computed(() => {
            return Object.keys(historicalDecisionData.value).find(key => key.includes(selectedHistory.value));
        });

        return {
            historicalDecisionData,
            matchingKey,
            selectedHistory
        };
    }
}
</script>

<style scoped>
.panel-heading {
    display: flex; 
    justify-content: space-between; 
    align-items: center;
}

.panel-body {
    background-color: #f4f4f4;
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
}

.input-wrapper {
    display: flex;         
    align-items: center;      
    margin-left: auto;         
}

.input-wrapper input {
    flex: 1;               
    padding: 8px;
    border: 1px solid #888;
    border-radius: 4px;
    margin-right: 5px;      
}

.input-wrapper .unit {
    color: #666;
    font-size: 0.9em;
}
</style>
