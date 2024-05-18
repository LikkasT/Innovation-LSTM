<template>
    <div class="container">
        <el-form class="form-con" ref="form" :model="form" label-width="80px">
            <el-form-item label="用户头像">
                <!-- 图片上传接口地址  替换-->
                <el-upload class="avatar-uploader" action="https://jsonplaceholder.typicode.com/posts/"
                    :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                    <img v-if="imageUrl" :src="imageUrl" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
            </el-form-item>

            <el-form-item label="用户ID">
                <el-input v-model="form.id"></el-input>
            </el-form-item>
            <el-form-item label="用户名称">
                <el-input v-model="form.info1"></el-input>
            </el-form-item>
            <el-form-item label="手机号码">
                <el-input v-model="form.info2"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱">
                <el-input v-model="form.info3"></el-input>
            </el-form-item>
            <el-form-item label="修改密码">
                <el-input type="password" v-model="form.password"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">修改</el-button>
                <el-button @click="goHome">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            imageUrl: '',
            form: {}
        };
    },
    mounted: {

    },
    methods: {
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
            const isLt2M = file.size / 1024 / 1024 < 2;

            if (!isJPG) {
                this.$message.error('上传头像图片只能是 JPG 格式!');
            }
            if (!isLt2M) {
                this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            return isJPG && isLt2M;
        }
    }
}
</script>

<style scoped>
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
</style>
