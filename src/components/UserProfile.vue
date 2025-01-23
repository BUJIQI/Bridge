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
                    <router-view />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/store/user';
import { ref, reactive } from 'vue';

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

        return {
            userProfile,
            editingProfile,
            isEditing,
            toggleEditMode,
            cancelEdit,
            saveProfile,
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
</style>