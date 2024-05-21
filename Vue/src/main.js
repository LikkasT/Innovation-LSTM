/* eslint-disable */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import * as auth from './utils/auth'

Vue.config.productionTip = false
Vue.use(ElementUI);

Vue.prototype.$message = ElementUI.Message;






new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
