<template>
    <div class="contanier">
        <el-container>
            <el-header>
                <el-row :gutter="20" class="flex-row">
                    <el-col :xs="6" :sm="6" :md="6" :lg="4" :xl="6">
                        <div class="flex-row avator-con" @click="gotoUserInfo">
                            <img :src="userURL !== '' ? userURL : defaultImagePath" alt="" srcset="">
                            <div class="flex-column avator-info">
                                <p>{{ userName || '未登录'}}</p>
                                <p>{{ userID || '' }}</p>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="12">
                        <div class="dollar-con">
                            <p @click="gototradingHistory">￥{{ userBalance }}</p>
                        </div>
                    </el-col>
                    <el-col :xs="6" :sm="6" :md="6" :lg="8" :xl="6">
                        <div class="search-con">
                            <el-autocomplete style="width: 100%;" v-model="state" :fetch-suggestions="querySearchAsync"
                                placeholder="请输入内容" suffix-icon="el-icon-search"
                                @select="handleSelect"></el-autocomplete>
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <el-menu router default-active="/profitHotlist" class="el-menu-vertical-demo">
                        <el-menu-item index="/profitHotlist">
                            <i class="el-icon-menu"></i>
                            <span slot="title">收益排行</span>
                        </el-menu-item>
                        <el-menu-item index="/tradingHotlist">

                            <i class="el-icon-menu"></i>
                            <span slot="title">交易热榜</span>
                        </el-menu-item>
                        <el-menu-item index="/userFollow">

                            <i class="el-icon-menu"></i>
                            <span slot="title">用户关注</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main> 
                    <!-- 使用路由缓存组件 -->
                    <keep-alive :include="['profitHotlist','tradingHotlist']">
                        <router-view></router-view>
                    </keep-alive>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
/* eslint-disable */

import { mapState, mapActions } from 'vuex'
import PubSub from 'pubsub-js';
import axios from 'axios';
import * as auth from '../utils/auth'
export default {
    name: 'Home',
    data() {
        return {
            defaultImagePath: require('@/assets/logo.png'),
            searchData: [],
            state     : '',
            timeout: null,
            eventTokens: {
                token1: null,
                token2: null,
                token3: null,
                token4: null,
            }
        }

    },
    computed: {
        // 从vuex中获取对应的数据。这个页面不会涉及对以下数据的修改
        ...mapState({
            userName: state => state.userData.userName,
            userID: state => state.userData.userID,
            userURL: state => state.userData.userURL,            
            userBalance: state => state.userData.userBalance,            
        })
    },
    async mounted() {
        try {
            const response = await this.loadAll();
            this.searchData = response.data;
            console.log('获取成功！');
        } catch(error) {
            console.log('获取失败！');
        } 
        this.eventTokens.token1 = PubSub.subscribe('goto');
        // 默认展示数据传给“收益排行”和“交易热榜”界面
        // this.eventTokens.token2 = PubSub.publish('getProfitHotlist', this.searchData);
        // this.eventTokens.token3 = PubSub.publish('getTradingHotlist', this.searchData);

        console.log(this.searchData);
    },
    beforeDestroy() {
        PubSub.unsubscribe(this.eventTokens.token1);
        // PubSub.unsubscribe(this.eventTokens.token2);
        // PubSub.unsubscribe(this.eventTokens.token3);
        
    },
    methods: {
        ...mapActions({
            autoLogin:'userLogin', 
        }),
       async loadAll() {
            try {
                const response = await axios({
                    method: 'GET',
                    baseURL: '/',
                    url: '/api/test',
                });
                return response;
            } catch (error) {
                throw error;
            }
        },
        querySearchAsync(queryString, cb) {
            var searchData = this.searchData;
            var results = queryString ? searchData.filter(this.createStateFilter(queryString)) : searchData;

            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                cb(results);
            }, 3000 * Math.random());
        },
        createStateFilter(queryString) {
            return (state) => {
                return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        handleSelect(item) {
            this.$router.push('/goodsInfo?id=' + item.id);
        },
        gototradingHistory() {
            this.$router.push('/tradingHistory');
        },
        gotoUserInfo() {
            if (this.userID) {
                this.$router.push('/userInfo');
            } else {
                PubSub.publish('gotoLogin');
                // this.$router.push('/userLogin');
            }
        }
    },
    created() {
        // 如果有Cookie，则自动登录
        console.log(auth.getUserCookie());
        if (auth.getUserCookie()) {
            this.autoLogin(auth.getUserCookie());
        }

    },
    mounted() {

    },
}
</script>

<style>
.el-aside {
    padding-top: 50px;
}

.el-menu-item {
    height: 60px;
    line-height: 60px;
    font-size: 16px;
}

.contanier {
    height: 100vh;
}

.el-container {
    min-height: calc(100vh - 100px);
}

.search-con input {
    height: 60px;
    line-height: 60px;
}

.min200 {
    min-width: 200px;
}

.dollar-con {
    font-size: 24px;
    font-weight: bold;
    text-align: left;
    padding-left: 20px;
}

.dollar-con p {
    cursor: pointer;
}

.avator-con {
    height: 100px;
}

.avator-info {
    line-height: 30px;
    margin-left: 10px;
    text-align: left;
}

.avator-con img {
    width: 80px;
    height: 80px;
    background-color: #333;
    border-radius: 50%;
    cursor: pointer;
}

.search-con {
    text-align: right;
}

.el-header,
.el-footer {
    background-color: #ffffff;
    color: #333;
    text-align: center;
    height: 100px !important;
    line-height: 100px;
    border-bottom: 5px #eee solid;
}

.el-aside {
    background-color: #ffffff;
    color: #333;
    text-align: center;
    line-height: 200px;
}

.el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    /* line-height: 160px; */
}

body>.el-container {
    margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
    line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
    line-height: 320px;
}
</style>