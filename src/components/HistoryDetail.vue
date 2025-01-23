<template>
    <div class="History-Game-Detail">
        <div class="header d-flex justify-content-between align-items-center">
            对局详情
            <button class="btn btn-link btn-sm" @click="goBack">
                <i class="fas fa-arrow-left"></i>
                返回
            </button>
        </div>
        <hr> <!-- 添加分割线 -->
        <div class="card">
            <div class="card-header">对局概览</div>
            <div class="card-body">
                <ul class="list-group">
                    <li class="list-group-item"><strong>轮次编号:</strong> {{ roundData.轮次编号 }}</li>
                    <li class="list-group-item"><strong>结束周期:</strong> {{ roundData.末周期 }}</li>
                    <li class="list-group-item"><strong>末周期评分:</strong> {{ roundData.末周期评分 }}</li>
                    <li class="list-group-item"><strong>名次:</strong> {{ roundData.末周期名次 }}</li>
                </ul>
            </div>
        </div>

        <div class="card">
            <div class="card-header">各周期评分</div>
            <div class="card-body">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th v-for="cycle in 7" :key="cycle">第{{ cycle }}周期</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td v-for="(score, index) in roundData.各周期评分" :key="index">{{ score }}</td>
                            <td v-for="empty in 7 - roundData.各周期评分.length" :key="'empty-' + empty">-</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card">
            <div class="card-header">各指标评分汇总</div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">市场类指标</div>
                            <div class="card-body">
                                <ul class="list-group">
                                    <li class="list-group-item" v-for="(value, key) in roundData['各指标评分汇总-市场类指标']"
                                        :key="key">
                                        {{ key }}: <span class="badge" style="background-color: lightcoral;">{{ value
                                            }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">生产类指标</div>
                            <div class="card-body">
                                <ul class="list-group">
                                    <li class="list-group-item" v-for="(value, key) in roundData['各指标评分汇总-生产类指标']"
                                        :key="key">
                                        {{ key }}: <span class="badge" style="background-color: lightcoral;">{{ value
                                            }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">财务类指标</div>
                            <div class="card-body">
                                <ul class="list-group">
                                    <li class="list-group-item" v-for="(value, key) in roundData['各指标评分汇总-财务类指标']"
                                        :key="key">
                                        {{ key }}: <span class="badge" style="background-color: lightcoral;">{{ value
                                            }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
    setup() {
        const route = useRoute();
        const router = useRouter();
        const roundData = ref({
            各周期评分: [] // 初始化时设置默认值为一个空数组
        });

        const goBack = () => {
            router.go(-1);
        };

        onMounted(() => {
            const roundDataStr = route.query.roundData;
            if (roundDataStr) {
                roundData.value = JSON.parse(roundDataStr);
            }
        });

        return {
            roundData,
            goBack,
        };
    }
};
</script>

<style scoped>
.panel {
    margin-top: 20px;
    border-radius: 8px;
}

.panel-body {
    padding: 15px;
}

.History-Game-Detail {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 50px;
}

.History-Game-Detail .header {
    font-size: 18px;
    color: #333;
    margin-bottom: 10px;
}

.History-Game-Detail .header button {
    font-size: 0.875rem;
    text-decoration: none;
    color: #444;
}

.History-Game-Detail .header button:hover {
    color: #000000;
}

.card {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px rgba(255, 33, 33, 0.292);
}

.card .card-header {
    background-color: #ffdede;
    border-bottom: none;
}

.table th,
.table td {
    text-align: center;
}
</style>