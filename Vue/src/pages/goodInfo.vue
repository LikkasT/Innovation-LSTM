<template>
    <div class="container">
        <div class="head-con flex-row">
            <img src="@/assets/logo.png" alt="" srcset="">
            <div class="r-con">
                <div class="flex-row flex-between">
                    <p>名称</p>
                    <img @click="guanzhu" :src="imageUrl" alt="">
                </div>
                <el-tabs class="tab-con" v-model="activeName" type="card">
                    <el-tab-pane label="1" name="1"></el-tab-pane>
                    <el-tab-pane label="2" name="2"></el-tab-pane>
                    <el-tab-pane label="3" name="3"></el-tab-pane>
                    <el-tab-pane label="4" name="4"></el-tab-pane>
                </el-tabs>
            </div>
        </div>
        <!-- 价格可视化二维表 -->
        <el-card class="box-card">
            <div slot="header" class="flex-row flex-between">
                <span>价格可视化二维表</span>
                <el-select @change="getDate" v-model="value" placeholder="请选择">
                    <el-option label="7日" value="7日">
                    </el-option>
                    <el-option label="30日" value="30日">
                    </el-option>
                </el-select>
            </div>
            <div id="main">

            </div>
        </el-card>



    </div>
</template>

<script>
/* eslint-disable */
import * as echarts from 'echarts';

export default {
    data() {
        return {
            activeName: '1',
            value: '7日',
            option: null,
            myChart: null,
            imageUrl: require('@/assets/no-guanzhu.png'),
            isGuanzhu: false
        }
    },
    mounted() {

        var chartDom = document.getElementById('main');
        this.myChart = echarts.init(chartDom);


        this.option = {
            title: {
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['lstm预测曲线', '其他模型预测曲线'],
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {

            },
            xAxis: {
                type: 'category',
                name: '时间',
                boundaryGap: false,
                data: ['1', '2', '3', '4', '5', '6', '7']
            },
            yAxis: {
                type: 'value',
                name: '价格',
                axisLine: {
                    show: true
                }
            },
            series: [
                {
                    name: 'lstm预测曲线',
                    type: 'line',
                    stack: 'Total',
                    data: [120, 132, 101, 134, 90, 230, 210]
                },
                {
                    name: '其他模型预测曲线',
                    type: 'line',
                    stack: 'Total',
                    data: [220, 182, 191, 234, 290, 330, 310]
                },

            ]
        };

        this.option && this.myChart.setOption(this.option);
    },
    methods: {
        // 关注取关
        guanzhu() {
            this.isGuanzhu = !this.isGuanzhu;
            this.imageUrl = this.isGuanzhu ? require('@/assets/guanzhu.png') : require('@/assets/no-guanzhu.png');
        },
        // 时间切换
        getDate(e) {
            if (e == "7日") {
                var xAxisData = [];
                var seriesData1 = [];
                var seriesData2 = [];

                for (var i = 1; i <= 7; i++) {
                    xAxisData.push(i);
                    // 假设这里是根据某种逻辑生成的新数据
                    seriesData1.push(Math.floor(Math.random() * 200));
                    seriesData2.push(Math.floor(Math.random() * 300));
                }

                this.option.xAxis.data = xAxisData;
                this.option.series[0].data = seriesData1;
                this.option.series[1].data = seriesData2;
            } else {
                var xAxisData = [];
                var seriesData1 = [];
                var seriesData2 = [];

                for (var i = 1; i <= 30; i++) {
                    xAxisData.push(i);
                    // 假设这里是根据某种逻辑生成的新数据
                    seriesData1.push(Math.floor(Math.random() * 200));
                    seriesData2.push(Math.floor(Math.random() * 300));
                }

                this.option.xAxis.data = xAxisData;
                this.option.series[0].data = seriesData1;
                this.option.series[1].data = seriesData2;
            }
            this.myChart.setOption(this.option);
        }
    },
}
</script>

<style scoped>
.container {
    background-color: #fff;
}

#main {
    width: 100%;
    height: 400px;
}

.head-con {
    justify-content: center;
}

.r-con {
    margin-left: 20px;
    padding: 20px;
}

.r-con img {
    width: 20px;
    height: 20px;
}

.r-con p {
    font-size: 18px;
    font-weight: bold;
}

.tab-con {
    margin-top: 100px;
}
</style>