const path = require('path');
const workingDir = __dirname;

const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const WebpackCleanupPlugin = require('webpack-cleanup-plugin');

const extractVendor = new ExtractTextPlugin("css/vendor.[contenthash].css");
const extractApp = new ExtractTextPlugin("css/app.[contenthash].css");

module.exports = {
  watch: false,
  entry: {
    app: __dirname + '/js/src/app.jsx',
    'libs': [
      'babel-polyfill',
      'bootstrap',
      '@fortawesome/fontawesome',
      'react',
      'react-dom'
    ]
  },
  devtool: 'source-map',
  output: {
    path: __dirname + '/dist',
    filename: '[name].bundle.[chunkhash].js'
  },
  resolve: {
    modules: ["node_modules"],
    alias: {
      cssDir: path.resolve(__dirname, 'css/')
    },
    extensions: ['.js', '.jsx']
  },
  plugins: [
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery',
      "window.jQuery": "jquery"
    }),
    new webpack.optimize.CommonsChunkPlugin({
      names: ['libs']
    }),
    new HtmlWebpackPlugin({
      filename: __dirname + '/index.html',
      template: __dirname + '/templates/index.html',
      inject: 'body'
    }),
    new WebpackCleanupPlugin({
      exclude: ["fonts/**/*"],
    }),
    extractVendor,
    extractApp
  ],
  module: {
    rules: [{
        test: /\.jsx$/,
        include: path.join(__dirname, 'js', 'src'),
        use: {
          loader: 'babel-loader',
          options: {
            "presets": ["env", "react"],
            "plugins": ["transform-object-rest-spread"]
          }
        }
      },
      // {
      //   test: /\.html$/,
      //   use: [{
      //     loader: 'html-loader',
      //     options: {
      //       minimize: true,
      //       root: path.resolve(__dirname, 'public'),
      //     }
      //   }]
      // },
      {
        test: /\.css$/,
        include: [
          path.resolve(__dirname, "node_modules")
        ],
        exclude: [
          path.resolve(__dirname, "css")
        ],
        use: extractVendor.extract({
          use: 'css-loader'
        })
      },
      {
        test: /\.css$/,
        include: [
          path.resolve(__dirname, "css")
        ],
        exclude: [
          path.resolve(__dirname, "node_modules")
        ],
        use: extractApp.extract({
          use: 'css-loader'
        })
      },
      {
        test: /\.(jpg|jpeg|gif|png|PNG)$/,
        loader: 'file-loader?limit=1024&publicPath=/dist/&name=images/[name].[ext]'
      },
      {
        test: /\.(woff|woff2|eot|ttf|svg)$/,
        loader: 'file-loader?emitFile=true,limit=1024&name=fonts/[name].[ext]'
      },
    ]
  }
};
