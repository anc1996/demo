# test

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### 目录结果
```
常用的Vue项目的一个目录结构和每个文件的作用

 

project

　dist　　　　　　　　　build，编译生成的包

　node_modules　　　　通过npm下载的一些外部文件

　public　　　　　　　　这个和src的assets文件夹都是用来存储静态资源的。这里的资源不会经过webpack打包处理

　src    开发目录

　　assets　　　　　　   存放资源，img和css等

　　common　　　　　　公共的js文件

　　　const.js　　　　　 公共的常量

　　　utils.js　　　　　　公共的方法

　　　mixin.js　　　　　 混入

　　components　　　　整个项目的小组件目录

　　　common　　　　  可以在很多个项目里面进行复用的公共组件

　　　content　　　　　当前项目的公共组件

　　network　　　 　  　网络的配置相关

　　　request.js    　  　请求的axios

　　router　　 　　 　　 路由处理

　　store　　 　　 　　  Vuex 的公共状态管理

　　views　　 　     　　视图组件，比如首页视图等等

　　App.vue　 　 　   　最开始的组件，也就是入口文件

　　main.js　　  　    　最开始执行的文件

　.editorconfig　　　　　编写风格　

　.gitignore　　　      　git忽略文件

　babel.config.js　　babel就是将项目中的es6的语法，进行转换，以便运行在旧的环境中

　package.json　　　npm包管理文件，使用了npm install的包会被记录在这里，用于记录开发和运行时依赖的包

　package-lock.json　锁定安装包的版本号，保证开发人员的项目依赖一致

　vue.config.js/webpack.config.js　　配置文件，一个是vue的，一个是webpack的，webpack的vue和react的都可以用，vue是专注于vue项目的。
-----------------------------------
Vue的目录结构
https://blog.51cto.com/u_15127540/4252963
```