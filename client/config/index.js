'use strict'
// Template version: 1.3.1
// see http://vuejs-templates.github.io/webpack for documentation.

const path = require('path')

module.exports = {
  dev: {

    // Paths
    env: require('./dev.env'),
    port: process.env.PORT || 8080,
    //port: process.env.PORT || 8080,
    autoOpenBrowser: true,
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    host: '127.0.0.1',
    //配置 webpack 将接口代理到本地
    proxyTable: {
      '/api': {
        target: 'http://127.0.0.1:22333/', // 接口的域名  
        changeOrigin: true,
        pathRewrite:{
            '^/api':''            
        }
      }
      // ,
      // '/api/query/monthsta': {
      //   target: 'http://127.0.0.1:22028/api/query/monthsta', // 接口的域名
      //   secure: false,
      //   changeOrigin: true,
      // }
    },
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false
  },

  build: {
    // Template for index.html
    // index: path.resolve(__dirname, '../dist/index.html'),
    // Paths
    // assetsRoot: path.resolve(__dirname, '../dist'),
    index: path.resolve(__dirname, '../../index.html'),
    assetsRoot: path.resolve(__dirname, '../../'),
    assetsSubDirectory: 'static',
    assetsPublicPath: './',

    /**
     * Source Maps
     */

    productionSourceMap: true,
    // https://webpack.js.org/configuration/devtool/#production
    devtool: '#source-map',
    // devtool: '#cheap-module-eval-source-map',

    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false,
    productionGzipExtensions: ['js', 'css'],

    // Run the build command with an extra argument to
    // View the bundle analyzer report after build finishes:
    // `npm run build --report`
    // Set to `true` or `false` to always turn it on or off
    bundleAnalyzerReport: process.env.npm_config_report
  }
}
