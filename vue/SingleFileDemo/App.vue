<!--App.vue文件为单文件组件文件-->

<template>
  <div>单文件组件</div>
</template>

<script>
export default {
  name: "App",
  data:function (){
    return {
      name:'python'
    }
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