<template>
    <div class="container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="7日收益" name="1">
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
                    <el-table-column prop="add" label="涨幅">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="30日收益" name="2">
                <el-table :data="tableData2" style="width: 100%">
                    <el-table-column type="index" label="序号" width="180px">
                    </el-table-column>
                    <el-table-column prop="img" label="图片">
                        <template slot-scope="scope">
                            <img :src="scope.row.img" style="width: 100px; height: 100px;" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="name" label="名称">
                    </el-table-column>
                    <el-table-column prop="add" label="涨幅">
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
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }],
            tableData2: [{
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎',
                add: '60%'
            }]
        }
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