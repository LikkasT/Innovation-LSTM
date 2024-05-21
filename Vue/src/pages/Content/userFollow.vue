<template>
    <div class="container">
        <el-table :data="tableData" style="width: 100%">
            <el-table-column type="index" label="序号" width="180px">
            </el-table-column>
            <el-table-column prop="img" label="图片">
                <template slot-scope="scope">
                    <img @click="handleRowClick(scope.row)" :src="scope.row.img"
                        style="width: 100px; height: 100px;cursor: pointer;" />
                </template>
            </el-table-column>
            <el-table-column prop="name" label="名称">
            </el-table-column>
            <el-table-column prop="add1" label="七日涨幅">
            </el-table-column>
            <el-table-column prop="add2" label="三十日涨幅">
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button v-if="scope.row.unfollowed" type="danger" size="mini"
                        @click="confirmUnfollow(scope.row)">取消关注</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    name:'userFollow',
    data() {
        return {
            tableData: [{
                img: require('../../assets/logo.png'),
                name: '王小虎1',
                add1: '30%',
                add2: '60%',
                unfollowed: true
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎2',
                add1: '30%',
                add2: '60%',
                unfollowed: true
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎3',
                add1: '30%',
                add2: '60%',
                unfollowed: true
            }, {
                img: require('../../assets/logo.png'),
                name: '王小虎4',
                add1: '30%',
                add2: '60%',
                unfollowed: true
            }]
        }
    },
    methods: {
        confirmUnfollow(row) {
            this.$confirm('确定要取消关注吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                const index = this.tableData.indexOf(row);
                if (index !== -1) {
                    this.tableData.splice(index, 1); // 从tableData中删除该行数据
                }
            }).catch(() => {
                // 用户点击取消按钮时的操作
            });
        },
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