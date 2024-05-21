<template>
    <div class="container">
        <div class="flex-tabs">
            <el-tabs v-model="activeName" style="width: 100%;">
                <el-tab-pane label="7日收益" name="1">
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
                        <el-table-column prop="7daysProfit" label="涨幅">
                        </el-table-column>
                    </el-table>
                    <el-pagination

                        background=""
                        :hide-on-single-page="isOnepage"
                        layout="prev, pager, next"
                        :total="tableData.length">
                    </el-pagination>
                </el-tab-pane>
                <el-tab-pane label="30日收益" name="2">
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
                        <el-table-column prop="30daysProfit" label="涨幅">
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </div>

    </div>
</template>

<script>
import PubSub from 'pubsub-js';

export default {
    name:'profitHotlist',
    data() {
        return {
            activeName: '1',
            tableData: [],
        }
    },
    computed: {
        isOnepage(){
            return this.tableData.length > 10 ? false : true;
        }
    },
    mounted() {
        // 接收从indexPage组件传递过来的默认展示数据
        PubSub.subscribe('getProfitHotlist',(msg, data) =>{
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