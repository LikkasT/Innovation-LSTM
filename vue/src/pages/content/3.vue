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
                name: 'AK-47 | 可燃冰',
                add1: '7%',
                add2: '31%'
            }, {
                name: '双持贝瑞塔 | 左右开花',
                add1: '45%',
                add2: '31%'
            }, {
                name: 'USP 消音版 | 引擎故障灯',
                add1: '30%',
                add2: '110%'
            }, {
                name: 'XM1014 | 斯康里娅',
                add1: '30%',
                add2: '20%'
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