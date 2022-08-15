<!--App.vue文件为单文件组件文件-->

<template>
  <div>单文件组件
    <!--多组件嵌套使用 -->
    <Child01></Child01>
    <Child02></Child02>
  </div>

</template>

<script>
//导入components目录下的子文件 Child01为指定的组件名，可以任意命名，不一定按照文件名
import Child01 from './components/Child01.vue'
import Child02 from './components/Child02.vue'

export default {
  name: "App",
  data:function (){
    return {
      name:'python'
    }
  },
  components:{
    // 注册单文件，多组件嵌套使用
    Child01,Child02
  }
}

</script>
<!--样式中如果有scope关键字，表示这些样式是组件局部的，不会影响其他元素-->
<style scoped>

  div{
    color:red;
    font-weight:bold;
    text-indent:10px;
  }
</style>