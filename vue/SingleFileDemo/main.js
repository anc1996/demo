// main.js 文件定义vue及调用单文件组件，也是项目打包时所依赖的文件

// 导入vue文件、App文件
import Vue from "vue"
import App from "./App.vue"

new Vue({
    el:'#app',
    // 渲染单位组件
    render:function (create){
        return create(App)
    }
})