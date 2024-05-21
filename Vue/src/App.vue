<template>
  <div id="app">
    <userContainer class="user-container"></userContainer>
    <router-view />
  </div>
</template>

<script>
import userContainer from "./components/userContainer";
export default {
  name: "App",
  components: {
    userContainer,
  },
  data() {
    return {};
  },
};
</script>

<style>
#app {

  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-width: 1200px;
}

.el-tabs__nav-scroll {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.flex-tabs {
  display: flex;
  justify-content: center;
  align-items: center;
}

* {
  margin: 0;
  padding: 0;
}

.container {
  padding: 20px;
}

.flex-row {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.flex-between {
  justify-content: space-between;
}

.flex-column {
  display: flex;
  flex-direction: column;
}
/* .user-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);  
  height: 500px;
  width: 400px;
  border: 1px solid red;
  margin: 0 auto;
  background-color: azure;
  z-index: 9999;
} */
</style>
