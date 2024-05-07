<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
</style>
