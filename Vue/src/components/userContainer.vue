<template>
  <div class="user-container">
    <el-dialog
      :title="status ? '登录' : '注册'"
      :visible.sync="dialogVisible"
      width="30%"
      show-close="false"
      :before-close="handleClose"
      @closed="handleClosed"
    >
      <userLogin    v-if = "status"  @closeDialog ="dialogVisible = false"/>
      <userRegister v-if = "!status" @closeDialog ="dialogVisible = false" />
      <span         slot = "footer" class = "dialog-footer">
        <!-- <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        <el-button @click="dialogVisible = false">取 消</el-button> -->
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PubSub from "pubsub-js";
import userLogin from "./userLogin.vue";
import userRegister from "./userRegister.vue";

export default {
  name: "userContainer",
  components: {
    userLogin,
    userRegister,
  },
  data() {
      return {
        status       : true,
        dialogVisible: false,
        eventtokens  : {
            token1: null,
            token2: null,
            token3: null,
            token4: null,
      },
    };
  },
  methods: {
      handleClose(done) {
        this.dialogVisible = true;
        done();
      },
      handleClosed() {
        this.status = true;
      }
  },
  created() {
          //当用户处于未登录状态时，跳转至注册页面的方法
    this.eventtokens.token1 = PubSub.subscribe("gotoUserRegister", () => {
      this.status = false;
    });
        // 当用户处于未登录状态时，跳转至登录界面的方法
    this.eventtokens.token2 = PubSub.subscribe("gotoLogin", () => {
        this.dialogVisible = true;
        this.status        = true;
    });
  },
  mounted() {

  },
  beforeDestroy() {
    PubSub.unsubscribe(this.eventtokens.token1);
    PubSub.unsubscribe(this.eventtokens.token2);
    PubSub.unsubscribe(this.eventtokens.token3);
  },
};
</script>

<style scoped>
/* .user-container {
  width: 400px;
  height: 500px;
  border: 1px solid red;
} */
</style>
