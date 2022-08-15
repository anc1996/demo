<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <test></test>
  </div>
</template>

<script>
// 导入别人组件
import HelloWorld from './components/HelloWorld.vue';
import test from './components/test';
export default {
  name: 'App',
  components: {
    // 局部注册并使用HelloWorld
    HelloWorld,
    test
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
