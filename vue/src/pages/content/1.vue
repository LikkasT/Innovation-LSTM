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
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                add: '7%'
            }, {
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                add: '7%'
            }, {
                img: require('../../assets/图片3.png'),
                name: '印花 | Vitality（全息）| 2023年巴黎锦标赛',
                add: '16%'
            }, {
                img: require('../../assets/图片4.png'),
                name: '双持贝瑞塔 | 左右开花',
                add: '45%'
            }],
            tableData2: [{
                img: require('../../assets/图片5.png'),
                name: 'USP 消音版 | 引擎故障灯',
                add: '110%'
            }, {
                img: require('../../assets/图片2.png'),
                name: 'AK-47 | 可燃冰',
                add: '31%'
            }, {
                img: require('../../assets/图片6.png'),
                name: 'XM1014 | 斯康里娅',
                add: '20%'
            }, {
                img: require('../../assets/图片7.png'),
                name: 'M4A4 | 沙漠精英',
                add: '13%'
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