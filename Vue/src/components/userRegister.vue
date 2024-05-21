<template>
  <div class="register">
    
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="ruleForm-register">
      <el-form-item label="用户名称" prop="userName">
        <el-input v-model="ruleForm.userName"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="手机号码" prop="phoneNumber">
        <el-input v-model="ruleForm.phoneNumber"></el-input>
      </el-form-item>
      <el-form-item label="SteamID" prop="steamID">
        <el-input v-model="ruleForm.steamID"></el-input>
      </el-form-item>
      <el-form-item label="电子邮箱" prop="email">
        <el-input v-model="ruleForm.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="info" @click="returnToLogin">
          返回登录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'
import PubSub from 'pubsub-js';
import { API_BASE_URL } from "../assets/config";
import { mapActions } from 'vuex';

export default {
  name: "userRegister",
  data() {
    var checkUserName = (rule, value, callback) => {
      if (!(/^[a-zA-Z0-9_]+$/.test(value))) {
        return callback(new Error('用户名应由字母、数字和下划线组成！'));
      } else {
        callback();
      }
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length < 6 || value.length > 12) {
        callback(new Error('长度不符合要求，请输入6-12位长度的密码'));
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass');
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    var checkEmail = (rule, value, callback) => {
      const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!(regex.test(value))) {
        return callback(new Error('输入的电子邮箱不符合格式！请重新输入！'));
      } else {
        callback();
      }
    }
    var checkPhoneNumber = (rule, value, callback) => {
      if (!(/^1\d{10}$/.test(value))) {
        callback(new Error('请输入正确的手机号码！'));
      } else {
        callback();
      }
    }
    return {
      ruleForm: {
        userName   : '',
        pass       : '',
        checkPass  : '',
        steamID    : '',
        email      : '',
        phoneNumber: ''
      },
      rules: {
        userName: [
          { validator: checkUserName, trigger: 'blur' }
        ],
        pass: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        email: [
          { validator: checkEmail, trigger: 'blur' }
        ],
        phoneNumber: [
          { validator: checkPhoneNumber, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    ...mapActions({
      register: 'userRegister',
      // setUserData: 'getRegisterForm'      
        }),
    submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          try {
            const response = await this.register(this.ruleForm);
            this.$message({
              message: response,
              type: 'success',
            });
            this.$emit('closeDialog');
          } catch (error) {
            this.$message.error(error);
          }

          // const registerData = {
          //   username    : this.ruleForm.userName,
          //   password    : this.ruleForm.pass,
          //   steamid     : this.ruleForm.steamID,
          //   phone_number: this.ruleForm.phoneNumber,
          //   email       : this.ruleForm.email
          // }

          // axios({
          //   method: 'POST',
          //   baseURL: API_BASE_URL,
          //   url: '/api/create_user',
          //   data:registerData,
          // })
          // .then(response => {
            
          //   // 这里要跳转至主页
          //   }).catch(error => {

          //   })

        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    returnToLogin() {
      PubSub.publish('gotoLogin');
    }
  }
}
</script>

<style scoped>
.ruleForm-register {
  max-width: 500px;
  margin: 0 auto;
}
</style>