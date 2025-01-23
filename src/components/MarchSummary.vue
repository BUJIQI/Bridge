<template>
    <div class="table-container">
        <div class="header">正在进行的对局</div>
        <table>
            <thead>
                <tr>
                    <th>开始时间</th>
                    <th>当前周期</th>
                    <th>末周期评分</th>
                    <th>名次</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="game in ongoingGames" :key="game.id" @click="goToDecisionInput(game.id)">
                    <td>{{ game.startTime }}</td>
                    <td>{{ game.currentCycle }}</td>
                    <td>{{ game.finalRating === '未评分' ? '---' : game.finalRating }}</td>
                    <td>{{ game.rank === '未评分/2' ? '---' : game.rank }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="table-container">
        <div class="header">
            历史对局
            <div class="view-more-container" @click="viewMoreAll">
                查看更多
                <span class="arrow"></span>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>结束时间</th>
                    <th>结束周期</th>
                    <th>末周期评分</th>
                    <th>名次</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="game in historyGames" :key="game.id" @click="fetchRoundHistory(game.endTime)">
                    <td>{{ game.endTime }}</td>
                    <td>{{ game.endCycle }}</td>
                    <td>{{ game.finalRating === '未评分' ? '---' : game.finalRating }}</td>
                    <td>{{ game.rank === '未评分/2' ? '---' : game.rank }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from '@/api/axios';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2';

export default {
    setup() {
        const router = useRouter();
        const ongoingGames = ref([]);
        const historyGames = ref([]);

        // 在组件挂载时发送GET请求
        onMounted(async () => {
            try {
                const response = await axios.get('/users/user_data/', {withCredentials: true});
                const data = response.data;

                // 处理历史轮次
                if (data.history_rounds !== "无历史对局") {
                    historyGames.value = Object.entries(data.history_rounds).map(([endTime, details]) => ({
                        id: Date.now() + Math.random(), // 生成唯一的id
                        endTime: endTime,
                        endCycle: details["结束周期"],
                        finalRating: details["末周期评分"],
                        rank: `${details["名次"]}/2`
                    }))
                    .sort((a, b) => new Date(b.endTime) - new Date(a.endTime))
                    .slice(0, 5);
                } else {
                    historyGames.value = [];
                }

                // 处理当前周期
                ongoingGames.value = Object.entries(data.current_rounds).map(([startTime, details]) => ({
                    id: Date.now() + Math.random(), // 生成唯一的id
                    startTime: startTime,
                    currentCycle: details["当前周期"],
                    finalRating: details["末周期评分"],
                    rank: `${details["名次"]}/2`
                }));

            } catch (error) {
                console.error("获取用户数据失败:", error);
            }
        });

        const goToDecisionInput = (gameId) => {
            router.push({ path: '/decision/input', query: { gameId: gameId } });
        };

        const viewMoreAll = () => {
            router.push({ path: '/profile/all-history-games' });
        };
        
        const fetchRoundHistory = async (endTime) => {
            try {
                const response = await axios.post('/users/round_hisdistail/', { endtime: endTime }, { withCredentials: true });
                const data = response.data;

                if (data.状态 === "该轮次周期未进行对决") {
                    Swal.fire({
                        title: '提示',
                        text: '该轮次周期未进行对决，无对局详情可查看',
                        icon: 'info',
                        confirmButtonText: '确定'
                    });
                } else {
                    router.push({ path: '/profile/history-detail', query: { roundData: JSON.stringify(data) } });
                }
            } catch (error) {
                console.error("获取对局详情失败:", error);
                alert('获取对局详情失败，请稍后再试');
            }
        };

        return {
            ongoingGames,
            historyGames,
            goToDecisionInput,
            viewMoreAll,
            fetchRoundHistory,
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

.table-container {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 50px;
}

.table-container .header {
    font-size: 18px;
    color: #333;
    margin-bottom: 10px;
}

.table-container table {
    width: 100%;
    border-collapse: collapse;
}

.table-container th, .table-container td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

.table-container th {
    background-color: rgb(197, 107, 107);
    color: white;
}

.table-container tr:nth-child(even) {
    background-color: #f2f2f2;
}

.table-container tr:hover {
    color:rgb(232, 76, 76);
    text-decoration: underline;
    cursor: pointer;
}

.table-container .header::after {
    content: "";
    display: table;
    clear: both;
}

.view-more-container {
    float: right;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    color:#444;
}

.arrow {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-bottom: 1.5px solid #444; 
  border-right: 1.5px solid #444; 
  transform: rotate(-45deg);
  transition: transform 0.3s ease;
  margin-left: 4px; 
}

.view-more-container:hover {
  color: #000000;
}

.view-more-container:hover .arrow {
  border-bottom: 1.5px solid #000000; 
  border-right: 1.5px solid #000000; 
}
</style>