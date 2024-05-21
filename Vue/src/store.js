import Vue from "vue";
import Vuex from 'vuex'
import {userLogin, userRegister,} from "./api/api";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userData: {
            userID: '',
            userName: '布偶熊',
            userPass: '',
            userPhoneNumber: '',
            userSteamID: '',
            userEmail: '',
            userURL: '',
            userBalance: '??????'
        },
        userFollows: {
            // 存储用户的关注商品
        },
        userTradingHistory: {
            // 存储用户的交易记录
        },

        searchData: []
    },
    getters: {
        // 对store的数据进行处理生成新的数据，类型Vue的计算属性
        // 该部分的操作不会修改state的内容。
        getUserData(state) {
            return state.userData;
        },
    },
    mutations: {
        // 这部分的操作用于同步改变Vuex中store数据的状态。
        // 不能在这部分执行异步操作
        // add(state, payload) {
        //     // state是默认参数
        // payload是额外传入的参数，当参数有多个时，payload为一个对象
        // }

        upUserData(state, payload) {
            state.userData.userID = payload.userID;
            state.userData.userName = payload.userName;
            state.userData.userPass = payload.userPass;
            state.userData.userPhoneNumber = payload.userPhoneNumber;
            state.userData.userSteamID = payload.userSteamID;
            state.userData.userEmail = payload.userEmail;
            state.userData.userURL = payload.userURL;
            state.userData.userBalance = payload.userBalance;
        }
    },
    actions: {
        // actions提交mutation操作
        // 这部分专门处理异步操作


        // 登录
        async userLogin(context, loginData) {
            try {
                const response = await userLogin(loginData);
                // console.log(response.data);
                context.commit('upUserData', response.data);
                return response.data.message;
            } catch (error) {
                // 把后端返回的错误信息抛出
                throw error.response.data.error;
            }
        },
        // 注册
        async userRegister(context, registerData) {
            try {
                const response = await userRegister(registerData);
                // dispatch('getRegisterForm', response.data);
                context.commit('upUserData', response.data);
                return response.data.message;
            } catch (error) {
                throw error.response.data.error;
            }
        },
        // 修改个人信息
        // async updateUserInfo(context, updatedData) {
        //     try {

        //     } catch (error) {

        //     }
        // }
        // 搜索

        // 用户关注/取消关注商品

        // 添加商品历史记录

        // 分页跳转
    }
})

// submitForm() {
//     userLogin({
//         phone_number: this.ruleForm.phoneNumber,
//         password: this.ruleForm.password,
//     })
//         .then((response) => {
//             // 要获取登录用户的所有个人信息，并自动跳转至主页
//             PubSub.subscribe('getUserData', (msg, userData) => {
//                 userData.userID = response.data.userID;
//                 userData.userName = response.data.userName;
//                 userData.userPassword = response.data.password;
//                 userData.userPhoneNumber = response.data.phone_number;
//                 userData.userSteamID = response.data.steamid;
//                 userData.userEmail = response.data.email;
//                 // userData.userAvatar = response.data.picture;
//             })
//         })
//         .catch((error) => {
//             // 打印对应的错误提示
//             console.log(error.error);
//         })

// },
