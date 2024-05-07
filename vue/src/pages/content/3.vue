<template>
    <div class="container">
        <el-table :data="tableData" style="width: 100%">
            <el-table-column type="index" label="序号" width="180px">
            </el-table-column>
            <el-table-column prop="name" label="名称">
            </el-table-column>
            <el-table-column prop="add1" label="七日涨幅">
            </el-table-column>
            <el-table-column prop="add2" label="三十日涨幅">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableData: [{
                name: '王小虎',
                add1: '30%',
                add2: '60%'
            }, {
                name: '王小虎',
                add1: '30%',
                add2: '60%'
            }, {
                name: '王小虎',
                add1: '30%',
                add2: '60%'
            }, {
                name: '王小虎',
                add1: '30%',
                add2: '60%'
            }]
        }
    },
}
</script>

<style scoped>
.container {
    background-color: #fff;
}
</style>