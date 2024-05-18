<template>
    <div class="contanier">
        <el-container>
            <el-header>
                <el-row>
                    <el-col :span="4">
                        <div class="flex-row avator-con" @click="gotoUserInfo">
                            <img src="@/assets/Yinxing2.png" alt="" srcset="">
                            <div class="flex-column avator-info">
                                <p>隐星</p>
                                <p>114514</p>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="14">
                        <div class="dollar-con">
                            <p @click="gotoJiaoyi">$1919810</p>
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="search-con">
                            <el-autocomplete v-model="state" :fetch-suggestions="querySearchAsync" placeholder="请输入内容"
                                suffix-icon="el-icon-search" @select="handleSelect"></el-autocomplete>
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-container>
                <el-aside width="250px">
                    <el-menu router default-active="/content1" class="el-menu-vertical-demo">
                        <el-menu-item index="/content1">
                            <i class="el-icon-menu"></i>
                            <span slot="title">收益排行</span>
                        </el-menu-item>
                        <el-menu-item index="/content2">

                            <i class="el-icon-menu"></i>
                            <span slot="title">交易热榜</span>
                        </el-menu-item>
                        <el-menu-item index="/content3">

                            <i class="el-icon-menu"></i>
                            <span slot="title">用户关注</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main> <router-view></router-view></el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
export default {
    name: 'Home',
    data() {
        return {
            input2: '',
            searchData: [],
            state: '',
            timeout: null
        }
    },
    mounted() {
        this.searchData = this.loadAll();
    },
    methods: {
        loadAll() {
            return [
                { "value": "商品1", "id": "1" },
                { "value": "商品2", "id": "2" }, ,
                { "value": "商品3", "id": "3" }, ,

            ];
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
        gotoJiaoyi() {
            this.$router.push('/jiaoyi');
        },
        gotoUserInfo() {
            this.$router.push('/userInfo');
        }
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

.dollar-con {
    font-size: 24px;
    font-weight: bold;
    text-align: left;
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

.el-header,
.el-footer {
    background-color: #f7f9fc;
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