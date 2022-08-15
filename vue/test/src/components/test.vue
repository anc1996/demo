<template>
  <!--模板区域-->
  <h2 class="red">test...</h2>
</template>

<script>
// 脚本区域
export default {
  name: "HelloWorld",
  props:{
    msg:{
      type:String,
      default:'test msg'
    }
  },
  data(){
    return{

    }
  }
}
</script>

<style scoped>
/*样式区域*/
.red{
  color: red;
}
</style>