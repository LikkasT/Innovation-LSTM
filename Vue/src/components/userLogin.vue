<template>
    <div class="login">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="ruleForm-login">
            <el-form-item label="手机号码" prop="phoneNumber">
                <el-input v-model="ruleForm.phoneNumber" placeholder="请输入手机号" class="login-Input"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input type="password" v-model="ruleForm.password" autocomplete="off" placeholder="请输入密码"
                    class="login-Input"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="login-button">登录</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="info" @click="gotoUserRegister" class="login-button">注册</el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script>
import PubSub from 'pubsub-js'
import {mapActions} from 'vuex';
import * as auth from '../utils/auth'

export default {
    name: "userLogin",
    data() {
        var checkPhoneNumber = (rule, value, callback) => {
            if (!(/^1\d{10}$/.test(value))) {
                callback(new Error('请输入正确的手机号码！'));
            } else {
                callback();
            }
        };
        return {
            ruleForm: {
                phoneNumber: '',
                password: '',

            },
            rules: {
                phoneNumber: [
                    { validator: checkPhoneNumber, trigger: 'blur' }
                ],
            },
            eventTokens: {
                token1: null,
                tokne2: null,

            }
        }
    },

    methods: {
        // 提交登录数据。若成功，则返回成功提示信息，若失败，则根据后端返回的提示信息提示用户
        ...mapActions({
            login: 'userLogin',
        }),
        // 验证并提交登录数据
        submitForm(formName) {
            this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    try {
                        const response = await this.login(this.ruleForm);
                        this.$message({
                            message: response,
                            type   : 'success'
                        });
                        // console.log(response);
                        // 将用户登录信息保存至Cookie
                        auth.setUserCookie(this.ruleForm);
                        // this.$router.push('/tradingHotlist');
                        this.$emit('closeDialog');
                    } catch (error) {
                        this.$message.error(error);
                    }
                }
            })
        },

        gotoUserRegister() {
            this.eventTokens.token1 = PubSub.publish('gotoUserRegister');
        }
    },
    created() {
    },
    beforeDestroy() {
        PubSub.unsubscribe(this.eventTokens.token1);
    }
}
</script>

<style scoped>
/* .login{
    position: relative;
    height: 500px;
    width: 400px;
    border: 1px solid red;
    margin: 0 auto;
    background-color: azure;
} */
/* .ruleForm-login {
    position: absolute;
    top: 50%;
    max-width: 100%;
    left: 50%;
    transform: translate(-50%,-50%); 
} */
.login-button {
    max-width: 500px;
}
</style>../api/api