<template>
    <div class="container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="7日热榜" name="1">
                <el-table :data="tableData" style="width: 100%" @row-click="handleRowClick">
                    <el-table-column type="index" label="序号" width="180px">
                    </el-table-column>
                    <el-table-column prop="img" label="图片">
                        <template slot-scope="scope">
                            <img :src="scope.row.img" style="width: 100px; height: 100px;" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="name" label="名称">
                    </el-table-column>
                    <el-table-column prop="jiaoyi" label="交易量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="30日热榜" name="2">
                <el-table :data="tableData2" style="width: 100%" @row-click="handleRowClick">
                    <el-table-column type="index" label="序号" width="180px">
                    </el-table-column>
                    <el-table-column prop="img" label="图片">
                        <template slot-scope="scope">
                            <img :src="scope.row.img" style="width: 100px; height: 100px;" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="name" label="名称">
                    </el-table-column>
                    <el-table-column prop="jiaoyi" label="交易量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
export default {
    data() {
        return {
            activeName: '1',
            tableData: [{
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }],
            tableData2: [{
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                jiaoyi: '20000'
            }],
        }
    },
}
</script>

<style scoped>
.container {
    background-color: #fff;
}
</style>