<template>
    <div class="contanier">
        <div class="cont-btn">
            <el-form ref="form" :model="form" :inline="true" label-width="80px">
                <el-form-item label="商品名">
                    <el-select v-model="form.value" filterable placeholder="请选择">
                        <el-option @click.native="select($event, item)" v-for="item in options" :key="item.value"
                            :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" icon="el-icon-plus" @click="add">新建交易历史</el-button>
                </el-form-item>
            </el-form>
        </div>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="img" label="图片">
                <template slot-scope="scope">
                    <img :src="scope.row.img" style="width: 100px; height: 100px;" />
                </template>
            </el-table-column>
            <el-table-column prop="name" label="名称">
            </el-table-column>
            <el-table-column prop="type" label="类型">
                <template slot-scope="scope">
                    <el-select v-model="scope.row.type" placeholder="类型">
                        <el-option label="买入" value="buy"></el-option>
                        <el-option label="卖出" value="sell"></el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="cprice" label="买入/卖出价格">
                <template slot-scope="scope">
                    <el-input v-model="scope.row.cprice" placeholder="买入/卖出价格"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="income" label="收益/支出">
                <template slot-scope="scope">
                    {{ calculateIncome(scope.row) }}
                </template>
            </el-table-column>
            <el-table-column prop="price" label="当前价">
            </el-table-column>
            <el-table-column prop="address" label="操作">
                <template slot-scope="scope">
                    <el-popconfirm title="这是一段内容确定删除吗？" @confirm="confirm(scope.row)">
                        <el-button slot="reference" size="mini" type="danger">删除</el-button>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            options: [{
                value: '1',
                label: '商品1',
                price: '300',
                img: require('../../assets/logo.png'),
            }, {
                value: '2',
                label: '商品2',
                price: '300',
                img: require('../../assets/logo.png'),
            }, {
                value: '3',
                label: '商品3',
                price: '300',
                img: require('../../assets/logo.png'),
            }, {
                value: '4',
                label: '商品4',
                price: '300',
                img: require('../../assets/logo.png'),
            }, {
                value: '5',
                label: '商品5',
                price: '300',
                img: require('../../assets/logo.png'),
            }],
            form: {},
            tableData: []

        }
    },
    methods: {
        calculateIncome(row) {
            if (row.type === 'sell') {
                return row.price - row.cprice;
            } else {
                return row.cprice;
            }
        },
        select(e, item) {
            console.log(e, item);
            this.selectData = item
        },
        add() {
            if (!this.form.value) {
                this.$message({
                    message: '请选择商品名称'
                });
                return false
            }
            let { value, label, img, price } = this.selectData
            let addData = {
                img,
                name: label,
                price
            }
            this.tableData.push(addData)
        },
        confirm(row) {
            const index = this.tableData.indexOf(row);
            if (index !== -1) {
                this.tableData.splice(index, 1);
            }
            this.$message({
                message: '删除成功',
                type: 'success'
            });
        },

    }
}
</script>

<style scoped>
.cont-btn {
    text-align: left;
    margin-bottom: 20px;
}
</style>