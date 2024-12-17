<template>
    <div class="panel panel-default mt-3">
        <div class="panel-body">
            <div class="row h-100">
                <div class="col-md-4">
                    <div class="user-profile" v-if="!isEditing">
                        <h4 class="card-header">个人信息</h4>
                        <hr> <!-- 添加分割线 -->
                        <p><strong>姓名:</strong> {{ userProfile.name }}</p>
                        <p><strong>学号:</strong> {{ userProfile.studentId }}</p>
                        <p><strong>队名:</strong> {{ userProfile.teamName }}</p>
                        <p><strong>班级:</strong> {{ userProfile.class }}</p>
                        <p><strong>组:</strong> 第{{ userProfile.group }}组</p>
                        <p><strong>企业:</strong> 第{{ userProfile.company }}企业</p>
                        <button class="btn btn-primary" @click="toggleEditMode">编辑资料</button>
                    </div>

                    <div class="edit-form" v-if="isEditing">
                        <h4 class="card-header">编辑个人资料</h4>
                        <hr> <!-- 添加分割线 -->
                        <div class="form-group">
                            <label for="name">姓名</label>
                            <input type="text" class="form-control" id="name" v-model="editingProfile.name">
                        </div>
                        <div class="form-group">
                            <label for="studentId">学号</label>
                            <input type="text" class="form-control" id="studentId" v-model="editingProfile.studentId">
                        </div>
                        <div class="form-group">
                            <label for="teamName">队名</label>
                            <input type="text" class="form-control" id="teamName" v-model="editingProfile.teamName">
                        </div>
                        <div class="form-group">
                            <label for="class">班级</label>
                            <input type="text" class="form-control" id="class" v-model="editingProfile.class">
                        </div>
                        <div class="form-group">
                            <label for="password">密码</label>
                            <input type="password" class="form-control" id="password" v-model="editingProfile.password">
                        </div>
                        <div class="form-group">
                            <label for="phone">手机</label>
                            <input type="tel" class="form-control" id="phone" v-model="editingProfile.phone">
                        </div>
                        <div class="form-group">
                            <label for="email">邮箱</label>
                            <input type="email" class="form-control" id="email" v-model="editingProfile.email">
                        </div>
                        <button type="button" class="btn btn-secondary" @click="cancelEdit">取消</button>
                        <button type="button" class="btn btn-thirdly" @click="saveProfile">保存</button>
                    </div>
                </div>

                <div class="col-md-8">
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
                                <tr v-for="game in ongoingGames" :key="game.id">
                                    <td>{{ game.startTime }}</td>
                                    <td>{{ game.currentCycle }}</td>
                                    <td>{{ game.finalRating === '未评分' ? '-' : game.finalRating }}</td>
                                    <td>{{ game.rank === '未评分/2' ? '-' : game.rank }}</td>
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
                                <tr v-for="game in historyGames" :key="game.id">
                                    <td>{{ game.endTime }}</td>
                                    <td>{{ game.endCycle }}</td>
                                    <td>{{ game.finalRating }}</td>
                                    <td>{{ game.rank }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios'; // 导入axios

export default {
    setup() {
        const userStore = useUserStore();
        const userInfo = userStore.userInfo;
        const userProfile = reactive({
            name: userInfo.username,
            studentId: userInfo.stuid,
            teamName: userInfo.team_name,
            class: userInfo.user_class,
            group: userInfo.group,
            company: userInfo.number,
            password: '',
            phone: '',
            email: ''
        });

        const editingProfile = reactive({
            name: '',
            studentId: '',
            teamName: '',
            class: '',
            group: '',
            company: '',
            password: '',
            phone: '',
            email: ''
        });

        const isEditing = ref(false);

        const ongoingGames = ref([]);
        const historyGames = ref([]);

        const toggleEditMode = () => {
            isEditing.value = !isEditing.value;
            if (isEditing.value) {
                Object.assign(editingProfile, userProfile);
            }
        };

        const cancelEdit = () => {
            isEditing.value = false;
        };

        const saveProfile = () => {
            Object.assign(userProfile, editingProfile);
            isEditing.value = false;
        };

        // 在组件挂载时发送GET请求
        onMounted(async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/users/user_data/', {withCredentials: true});
                const data = response.data;
                console.log(data);

                // 处理历史轮次
                if (data.history_rounds !== "无历史对局") {
                    historyGames.value = Object.entries(data.history_rounds).map(([endTime, details]) => ({
                        id: Date.now() + Math.random(), // 生成唯一的id
                        endTime: endTime,
                        endCycle: details["结束周期"],
                        finalRating: details["末周期评分"],
                        rank: `${details["名次"]}/2`
                    }));
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

        const viewMoreAll = () => {
            // 这里可以添加具体逻辑，比如跳转到详情页面或者弹出模态框
            console.log('查看更多历史对局');
        };        

        return {
            userProfile,
            editingProfile,
            isEditing,
            ongoingGames,
            historyGames,
            toggleEditMode,
            cancelEdit,
            saveProfile,
            viewMoreAll
        };
    }
};
</script>

<style scoped>
/* 根据需要添加样式 */
.panel {
    margin-top: 20px;
    border-radius: 8px;
}

.panel-body {
    padding: 15px;
}

.user-profile {
    background-color: #f8f9fa; 
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.user-name {
    font-size: 24px;
    color: #333; 
    margin-bottom: 10px;
}

.btn-primary {
    background-color: #c00; 
    border-color: #c00;  
}

.btn-primary:hover,
.btn-primary:focus {
    background-color: rgb(190, 0, 0); 
    border-color: rgb(190, 0, 0);
}

.btn-secondary {
    background-color: #6c757d; 
    border-color: #6c757d;
    color: #fff;
    margin: 10px 10px 0 0;
}

.btn-secondary:hover,
.btn-secondary:focus {
    background-color: #545b62;
    border-color: #545b62;
}

.btn-thirdly {
    background-color: #c00; 
    border-color: #c00; 
    color: #fff;
    margin: 10px 0 0 0;
}

.btn-thirdly:hover,
.btn-thirdly:focus {
    background-color: rgb(190, 0, 0); 
    border-color: rgb(190, 0, 0);
}

.edit-form {
    background-color: #f8f9fa; 
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
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
    background-color: #ddd;
}

.header {
    position: relative;  
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
}

.arrow {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-bottom: 2px solid #333; 
  border-right: 2px solid #333; 
  transform: rotate(-45deg);
  transition: transform 0.3s ease;
  margin-left: 8px; 
}
</style>