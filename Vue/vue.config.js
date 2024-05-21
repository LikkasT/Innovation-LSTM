const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:9511',
        changeOrigin: true,
        //pathRewrite: { '^/api': '' }
        onProxyRes(proxyRes, req, res) {
          //在控制台显示真实代理地址
          console.log(req.url);
        },
      }
    }
  }
})
