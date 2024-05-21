<template>
    <div class="container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="7日热榜" name="1">
                <el-table :data="tableData" style="width: 100%" v-if="activeName == '1'">
                    <el-table-column type="index" label="序号" width="180px">
                    </el-table-column>
                    <el-table-column prop="goodURL" label="图片">
                        <template slot-scope="scope">
                            <img @click="handleRowClick(scope.row)" :src="scope.row.goodURL"
                                style="width: 100px; height: 100px;cursor: pointer;" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="goodName" label="商品名称">
                    </el-table-column>
                    <el-table-column prop="7daysTrading" label="7日交易量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="30日热榜" name="2">
                <el-table :data="tableData" style="width: 100%" v-if="activeName == '2'">
                    <el-table-column type="index" label="序号" width="180px">
                    </el-table-column>
                    <el-table-column prop="goodURL" label="图片">
                        <template slot-scope="scope">
                            <img @click="handleRowClick(scope.row)" :src="scope.row.goodURL"
                                style="width: 100px; height: 100px;cursor: pointer;" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="goodName" label="商品名称">
                    </el-table-column>
                    <el-table-column prop="30daysTrading" label="30日交易量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import PubSub from 'pubsub-js';

export default {
    name:'tradingHotlist',
    data() {
        return {
            activeName: '1',
            tableData: [],

        }
    },
    mounted() {
        // 接收从indexPage组件传递过来的默认展示数据
        PubSub.subscribe('getTradingHotlist',(msg, data) =>{
            this.tableData = data;
        })
    },
    methods: {
        handleRowClick(row) {
            let id = row.id ? row.id : 1
            this.$router.push('/goodsInfo?id=' + id);
        }
    }
}
</script>

<style scoped>
.container {
    background-color: #fff;
}
</style>