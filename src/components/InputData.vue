<template>
    <div class="panel panel-default mt-3">
        <div class="panel-heading">
            <h3 class="panel-title">第{{ userInfo?.cycle }}周期决策数据输入</h3>
            <div class="mode-selection" style="float: right;">
                <span>选择模式：</span>
                <button :class="{ active: isOwnEnterprise }" @click="selectMode('own')">本企业</button>
                <button :class="{ active: !isOwnEnterprise }" @click="selectMode('competitor')">竞争企业</button>
            </div>
        </div>
        <div class="panel-body">
            <section class="decision-section sales">
                <h2>销售</h2>
                <div class="input-group">
                    <label>一般市场价格</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.general_market_price" />
                        <span class="unit">元/台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>广告费用投入</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.advertising_investment" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>销售人员个数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.sales_staff" />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>市场和生产研究报告</label>
                    <div class="input-wrapper">
                        <select v-model="formData.market_research_report">
                            <option value="Y">Y</option>
                            <option value="N">N</option>
                        </select>
                        <span class="unit">Y/N</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>附一：投标价格</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.bid_price" />
                        <span class="unit">元/台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>附二：特殊产品数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.special_product_qty" />
                        <span class="unit">台</span>
                    </div>
                </div>
            </section>

            <section class="decision-section production">
                <h2>生产</h2>
                <div class="input-group">
                    <label>一般市场产品计划量</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_plan_qty" />
                        <span class="unit">台</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产线投资数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_line_investment" />
                        <span class="unit">条</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产线变卖数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_line_change" />
                        <span class="unit">条</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>维修保养费用</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.maintenance_cost" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产合理化投资</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_optimization_investment" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产人员招收数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_staff_recruitment" />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>生产人员辞退数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.production_staff_resignation" />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买机器人</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.purchase_robot" />
                        <span class="unit">个</span>
                    </div>
                </div>
            </section>

            <section class="decision-section purchasing">
                <h2>采购</h2>
                <div class="input-group">
                    <label>购买原材料量</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.raw_material_purchase_qty" />
                        <span class="unit">单位</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买附件量</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.purchase_accessories" />
                        <span class="unit">单位</span>
                    </div>
                </div>
            </section>

            <section class="decision-section quality">
                <h2>质量</h2>
                <div class="input-group">
                    <label>科研人员招收数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.research_staff_recruitment" />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>科研人员辞退数</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.research_staff_resignation" />
                        <span class="unit">个</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>产品改进费用</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.product_improvement_cost" />
                        <span class="unit">百万元</span>
                    </div>
                </div>
            </section>

            <section class="decision-section finance">
                <h2>财务</h2>
                <div class="input-group">
                    <label>社会福利费用</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.social_benefits" />
                        <span class="unit">%</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>中期贷款</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.medium_term_loan" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>购买有价证券</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.purchase_securities" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>计划支付股息</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.planned_dividend_payment" />
                        <span class="unit">百万元</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>管理合理化投资</label>
                    <div class="input-wrapper">
                        <input type="text" v-model="formData.management_optimization_investment" />
                        <span class="unit">百万元</span>
                    </div>
                </div>
            </section>

            <div class="button-group">
                <button class="custom-button" @click="makeBudgetDecision">预算决策</button>
                <button class="custom-button" @click="submitDecision" :disabled="!isOwnEnterprise" :class="{ 'disabled-button': !isOwnEnterprise }">提交决策</button>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import { ref } from 'vue';
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
    setup() {
        const userStore = useUserStore();
        const userInfo = userStore.userInfo;
        const isOwnEnterprise = ref(true);

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

        return {
            userInfo,
            isOwnEnterprise,
            formData,
        };
    },

    methods: {
        selectMode(mode) {
            this.isOwnEnterprise = (mode === 'own');
        },

        makeBudgetDecision() {
            alert('进行预算决策');
        },

        async submitDecision() {
            const result = await Swal.fire({
                title: '确认提交',
                text: '您确定要提交决策数据吗？',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消'
            });

            if (result.isConfirmed) {
                try {
                    const response = await axios.post('http://127.0.0.1:8000/users/commit_decision/', this.formData, {
                        withCredentials: true
                        });
                    const submitResult = response.data;

                    if (submitResult['提交结果'] === '决策数据已经成功递交') {
                        Swal.fire('成功', '决策数据已经成功递交，可前往查看竞争结果报表', 'success');
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
        }

    }
}
</script>

<style scoped>
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

.mode-selection {
    display: flex;
    align-items: center;
}

.mode-selection button.active {
    background-color: rgba(176, 63, 63, 0.733);
    color: white;
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
}

.input-wrapper {
    display: flex;         
    align-items: center;      
    margin-left: auto;         
}

.input-wrapper input,
.input-wrapper select {
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

.button-group {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.custom-button {
    background-color: #e74c3c; 
    color: white;                
    margin-left: 40px;
    margin-right: 40px;         
    border-radius: 5px;        
    cursor: pointer;             
    transition: background-color 0.3s, transform 0.2s; 
}

.custom-button:hover {
    background-color: #c0392b;  
    transform: scale(1.05);      
}

.disabled-button {
    background-color: #cccccc; 
    color: #666666;              
    cursor: not-allowed;        
    pointer-events: none;        
}

.custom-button:active {
    transform: scale(0.95);     
}
</style>
