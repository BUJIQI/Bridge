<template>
    <div class="panel panel-default mt-3">
        <div class="panel-body">
            <div class="row h-100">
                <div class="col-md-4">
                    <div class="user-profile" v-if="!isEditing && !isChangingPassword">
                        <h4 class="card-header">个人信息</h4>
                        <hr>
                        <p><strong>姓名:</strong> {{ userProfile.name }}</p>
                        <p><strong>学号:</strong> {{ userProfile.studentId }}</p>
                        <p><strong>队名:</strong> {{ userProfile.teamName }}</p>
                        <p><strong>班级:</strong> {{ userProfile.class }}</p>
                        <p><strong>组:</strong> 第{{ userProfile.group }}组</p>
                        <p><strong>企业:</strong> 第{{ userProfile.company }}企业</p>
                        <button class="btn btn-primary" @click="toggleEditMode">编辑资料</button>
                        <button class="btn change-password" @click="toggleChangePassword">更改密码</button>
                    </div>

                    <div class="edit-form" v-if="isEditing">
                        <h4 class="card-header">编辑个人资料</h4>
                        <hr> 
                        <form @submit.prevent="saveProfile" novalidate class="needs-validation">
                            <div class="form-group">
                                <label for="name">姓名</label>
                                <input type="text" class="form-control" id="name" v-model="editingProfile.name" disabled>
                            </div>
                            <div class="form-group">
                                <label for="studentId">学号</label>
                                <input type="text" class="form-control" id="studentId" v-model="editingProfile.studentId" disabled>
                            </div>
                            <div class="form-group">
                                <label for="teamName">队名</label>
                                <input type="text" class="form-control" id="teamName" v-model="editingProfile.teamName" disabled>
                            </div>
                            <div class="form-group">
                                <label for="class">班级</label>
                                <input type="text" class="form-control" id="class" v-model="editingProfile.class" disabled>
                            </div>
                            <div class="form-group">
                                <label for="phone">手机</label>
                                <input type="tel" class="form-control" id="phone" v-model="editingProfile.phone" disabled>
                            </div>
                            <div class="form-group">
                                <label for="email">邮箱</label>
                                <input type="email" class="form-control" id="email" v-model="editingProfile.email" required>
                                <div class="invalid-feedback">
                                    请输入有效的邮箱地址。
                                </div>
                            </div>
                            <button type="button" class="btn btn-secondary" @click="cancelEdit">取消</button>
                            <button type="submit" class="btn btn-thirdly">保存</button>
                        </form>
                    </div>

                    <div class="change-password-form" v-if="isChangingPassword">
                        <h4 class="card-header">更改密码</h4>
                        <hr> 
                        <form @submit.prevent="changePassword" novalidate class="needs-validation">
                            <div class="form-group">
                                <label for="originalPassword">原密码</label>
                                <input type="password" class="form-control" id="originalPassword" v-model="changePasswordForm.original_password" maxlength="5" required>
                            </div>
                            <div class="form-group">
                                <label for="newPassword">新密码</label>
                                <input type="password" class="form-control" id="newPassword" v-model="changePasswordForm.new_password" maxlength="5" required>
                            </div>
                            <div class="form-group">
                                <label for="confirmPassword">确认密码</label>
                                <input type="password" class="form-control" id="confirmPassword" v-model="changePasswordForm.confirm_password" maxlength="5" required>
                            </div>
                            <button type="button" class="btn btn-secondary" @click="cancelChangePassword">取消</button>
                            <button type="submit" class="btn btn-thirdly">确定</button>
                        </form>
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
import axios from '@/api/axios';
import Swal from 'sweetalert2';

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
            phone: userInfo.phone,
            email: userInfo.email
        });

        const editingProfile = reactive({
            name: '',
            studentId: '',
            teamName: '',
            class: '',
            group: '',
            company: '',
            phone: '',
            email: ''
        });

        const isEditing = ref(false);
        const isChangingPassword = ref(false);

        const changePasswordForm = reactive({
            original_password: '',
            new_password: '',
            confirm_password: ''
        });

        const toggleEditMode = () => {
            isEditing.value = !isEditing.value;
            if (isEditing.value) {
                Object.assign(editingProfile, userProfile);
            }
        };

        const cancelEdit = () => {
            isEditing.value = false;
        };

        const toggleChangePassword = () => {
            isChangingPassword.value = !isChangingPassword.value;
        };

        const cancelChangePassword = () => {
            isChangingPassword.value = false;
        };

        const saveProfile = (event) => {
            const form = event.target.closest('form');
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
                return; // 确保只有在验证通过的情况下才继续执行
            }
            form.classList.add('was-validated');
            
            const newEmail = editingProfile.email;
            axios.post('/users/change_email/', { new_email: newEmail }, { withCredentials: true })
                .then(response => {
                    const data = response.data;
                    if (data.message === "邮箱修改成功") {
                        Object.assign(userProfile, editingProfile); // 更新userProfile
                        localStorage.setItem('userInfo', JSON.stringify({ ...userStore.userInfo, email: newEmail })); // 更新localStorage
                        Swal.fire({
                            icon: 'success',
                            title: '成功',
                            text: data.message,
                        });
                        isEditing.value = false;
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: '失败',
                            text: data.message,
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire({
                        icon: 'error',
                        title: '错误',
                        text: '邮箱修改失败，请重试。',
                    });
                });
        };

        const changePassword = (event) => {
            const form = event.target.closest('form');
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
                return; // 确保只有在验证通过的情况下才继续执行
            }
            form.classList.add('was-validated');

            axios.post('/users/change_password/', changePasswordForm, {withCredentials: true})
                .then(response => {
                    const data = response.data;
                    if (data.state === "True") {
                        Swal.fire({
                            icon: 'success',
                            title: '成功',
                            text: data.text,
                        });
                        isChangingPassword.value = false;
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: '失败',
                            text: data.text,
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire({
                        icon: 'error',
                        title: '错误',
                        text: '密码修改失败，请重试。',
                    });
                });
        };

        return {
            userProfile,
            editingProfile,
            isEditing,
            isChangingPassword,
            toggleEditMode,
            cancelEdit,
            toggleChangePassword,
            cancelChangePassword,
            saveProfile,
            changePassword,
            changePasswordForm,
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

.form-group {
    margin-bottom: 15px;
}

.btn-primary {
    background-color: rgb(251, 73, 73); 
    width: 100%;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 15px;
}

.btn-primary:hover,
.btn-primary:focus {
    background-color: rgb(235, 39, 39); 
}

.btn-secondary {
    background-color: #6c757d; 
    width: 45%;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 10px 30px 0 0;
}

.btn-secondary:hover,
.btn-secondary:focus {
    background-color: #545b62;
}

.btn-thirdly {
    background-color: rgb(251, 73, 73); 
    width: 45%;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    color: white;
    margin: 10px 0 0 0;
}

.btn-thirdly:hover,
.btn-thirdly:focus {
    background-color: rgb(235, 39, 39);  
    color: white;
}

.edit-form, .change-password-form {
    background-color: #f8f9fa; 
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.change-password {
    background-color: rgb(146, 146, 146); 
    width: 100%;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    color: white;
}

.change-password:hover,
.change-password:focus {
    background-color: #545b62;
    color: white;
}
</style>