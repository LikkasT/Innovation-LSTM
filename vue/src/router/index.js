import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/pages/index'
import Content1 from '@/pages/content/1';
import Content2 from '@/pages/content/2';
import Content3 from '@/pages/content/3';
import UserInfo from '@/pages/userInfo/index';
import GoodsInfo from '@/pages/goodsInfo/index';
import Jiaoyi from '@/pages/jiaoyi/index';
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      children: [{
        path: '/content1',
        component: Content1
      },
      {
        path: '/content2',
        component: Content2
      },
      {
        path: '/content3',
        component: Content3
      },
      {
        path: '/UserInfo',
        name: 'userInfo',
        component: UserInfo,
      },
      {
        path: '/GoodsInfo',
        name: 'goodsInfo',
        component: GoodsInfo,
      },
      {
        path: '/Jiaoyi',
        name: 'jiaoyi',
        component: Jiaoyi,
      }
      ]
    },


  ]
})
