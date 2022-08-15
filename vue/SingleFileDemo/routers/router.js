// 导入路由插件
import Vue from "vue";
import Router from 'vue-router';
import Child01 from "../components/Child01.vue";
import Child02 from "../components/Child02.vue";


// 指定Vue使用路由
Vue.use(Router)
// 指定匹配路由规则
export default new Router({
    routes:[
        {
            path:'/child01',
            component:Child01
        },
        {
            path:'/child02',
            component:Child02
        }
    ]
})