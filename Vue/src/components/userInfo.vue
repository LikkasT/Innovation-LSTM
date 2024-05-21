<template>
    <div class="container">
        <el-form class="form-con" ref="userInfo" :model="form" label-width="80px">
            <el-form-item label="用户头像" class="avatar-div">
                <!-- 图片上传接口地址  替换-->
                <el-upload class="avatar-uploader" action="https://jsonplaceholder.typicode.com/posts/"
                    :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                    <img v-if="imageUrl" :src="imageUrl" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
            </el-form-item>

            <el-form-item label="用户ID">
                <el-input v-model="userInfo.userID" :readonly="true" class="input-first"></el-input>
            </el-form-item>
            <el-form-item label="用户名称">
                <el-input v-model="userInfo.userName"></el-input>
            </el-form-item>
            <el-form-item label="手机号码">
                <el-input v-model="userInfo.userPhoneNumber"></el-input>
            </el-form-item>
            <el-form-item label="SteamID">
                <el-input v-model="userInfo.userSteamID"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱">
                <el-input v-model="userInfo.userEmail"></el-input>
            </el-form-item>
            <el-form-item label="新密码">
                <el-input type="password" v-model="userInfo.newPass" show-password></el-input>
            </el-form-item>     
            <el-form-item label="确认密码">
                <el-input type="password" v-model="userInfo.checkPass" show-password></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">修改</el-button>
                <el-button @click="goHome">取消</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="danger">退出登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import {mapActions, mapGetters, mapState} from 'vuex';

export default {
    data() {
        return {
            imageUrl: '',

            userInfo: {
                userID: '',
                userName: '',
                password:'',
                newPass: '',
                checkPass: '',
                userPhoneNumber: '',
                userSteamID: '',
                userEmail: '',
                userURL: '',
            },
        };
    },
    computed: {
        ...mapState({
            vuexUserInfo: state => state.userData
        }),
        ...mapGetters({
            getUserInfo: 'getUserData',
        })
    },
    watch: {
        // 监听用户信息
        vuexUserInfo: {
            handler(newVal) {
                const {
                    userID, userName, userPass, userPhoneNumber, userSteamID, userEmail, userURL,
                } = newVal;
                this.userInfo = {
                    userID,userName,userPass,userPhoneNumber,userSteamID,userEmail,userURL,
                    newPass: '',checkPass: '',
                }
            },
            deep: true,
        }

    }, 
    methods: {
        ...mapActions({
            update:'updateUserInfo'
        }),
        onSubmit() {

        },
        goHome() {
            this.$router.push('/');
        },
        handleAvatarSuccess(res, file) {
            this.imageUrl = URL.createObjectURL(file.raw);
        },
        beforeAvatarUpload(file) {
            const isJPG = file.type === 'image/jpeg';
            const isLt2M = file.size / 1024 / 1024 < 5;

            if (!isJPG) {
                this.$message.error('上传头像图片只能是 JPG 格式!');
            }
            if (!isLt2M) {
                this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            return isJPG && isLt2M;
        }
    },

    created() {
        // 确认处于登录状态，则创建组件时加载用户的信息
        const {
            userID,userName,userPass,userPhoneNumber,userSteamID,userEmail,userURL,
        } = this.$store.getters.getUserData;

        this.userInfo = {
            userID,userName,userPass,userPhoneNumber,userSteamID,userEmail,userURL,
            newPass: '',checkPass: '',
        }
    }
}
</script>

<style>
.container {
    background-color: #fff;
}

.form-con {
    width: 50%;
    margin: 0 auto;
}

.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
}

.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
.input-first input{
    border: none;
}

.avatar-div label{
    margin-top: 70px;
}
</style>