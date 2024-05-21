// 该文件专门用于创建整个项目的路由
import Vue from "vue";
import VueRouter from "vue-router";
import * as auth from '../utils/auth'
import {
    IndexPage,
    // userRegister,
    // userLogin,
    userInfo,
    tradingHotlist,
    profitHotlist,
    userFollow,
    goodInfo,
    tradingHistory,
} from './routes'
Vue.use(VueRouter);



// 创建并暴露一个路由器
const router = new VueRouter({
    routes: [
        {
            name: 'IndexPage',
            path: '/',
            component: IndexPage,
            meta: {
                requiresAuth: false,
            },
            redirect: '/profitHotlist',
            children: [
                {
                    name: 'userInfo',
                    path: 'userInfo',
                    component: userInfo,
                    meta: {
                        requiresAuth: true,
                    }
                },
                {
                    name: 'tradingHotlist',
                    path: 'tradingHotlist',
                    component: tradingHotlist,
                    meta: {
                        requiresAuth: false,
                    }
                },
                {
                    name: 'profitHotlist',
                    path: 'profitHotlist',
                    component: profitHotlist,
                    meta: {
                        requiresAuth: false,
                    }
                }, {
                    name: 'userFollow',
                    path: 'userFollow',
                    component: userFollow,
                    meta: {
                        requiresAuth: true,
                    }
                }, {
                    name: 'goodInfo',
                    path: 'goodInfo',
                    component: goodInfo,
                    meta: {
                        requiresAuth: false,
                    }
                }, {
                    name: 'tradingHistory',
                    path: 'tradingHistory',
                    component: tradingHistory,
                    meta: {
                        requiresAuth: true,
                    }
                },
                // {
                //     name: 'userLogin',
                //     path: 'userLogin',
                //     component: userLogin
                // },
                // {
                //     name: 'userRegister',
                //     path: 'userRegister',
                //     component: userRegister
                // },
            ]

        },
    ]
});

// 全局前置路由守卫:初始化时、每次路由切换之前被调用
// 接收参数：to from next
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        if (auth.getUserCookie()) {
            console.log(auth.getUserCookie());
            console.log('存在Cookie！');
            next();
        } else {
            console.log('没有Cookie!');
            // 返回主页并弹出登录框
            next('/');
        }
    } else {
        next();
    }
})

export default router;