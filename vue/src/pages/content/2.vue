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
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                jiaoyi: 1748
            }, {
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                jiaoyi: 1748
            }, {
                img: require('../../assets/图片3.png'),
                name: '印花 | Vitality（全息）| 2023年巴黎锦标赛',
                jiaoyi: 358
            }, {
                img: require('../../assets/图片4.png'),
                name: '双持贝瑞塔 | 左右开花',
                jiaoyi: 445
            }],
            tableData2: [{
                img: require('../../assets/图片5.png'),
                name: 'USP 消音版 | 引擎故障灯',
                jiaoyi: 1145
            }, {
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                jiaoyi: 2581
            }, {
                img: require('../../assets/图片6.png'),
                name: 'XM1014 | 斯康里娅',
                jiaoyi: 1101
            }, {
                img: require('../../assets/图片7.png'),
                name: 'M4A4 | 沙漠精英',
                jiaoyi: 789
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