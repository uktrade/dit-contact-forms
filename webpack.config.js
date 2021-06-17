const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require('webpack');
//const dotenv = require('dotenv').config();
//const dotenv = require('dotenv-webpack');

console.log("Will it display?:");
console.log(process.env);
//console.log(dotenv.config().parsed);

module.exports = {
  entry: {
    global: [
      "./assets/javascript/global.js",
      "./assets/scss/global.scss",
    ],
    cookiePolicyForm: [
      "./assets/javascript/cookie-policy-form.js",
    ],
  },

  output: {
    path: path.resolve("./assets/webpack_bundles/"),
    publicPath: "/static/webpack_bundles/",
    filename: "[name]-[fullhash].js"
  },

  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new MiniCssExtractPlugin({
        filename: "[name]-[fullhash].css",
        chunkFilename: "[id]-[fullhash].css",
    }),
    new CopyPlugin({
      patterns: [
        { from: "./assets/images/", to: "images"}
      ]
    }),
    new webpack.DefinePlugin({
      //'process.env': JSON.stringify(dotenv.config().parsed),
      'SENTRY_DSN': JSON.stringify(process.env.SENTRY_DSN),
      'SENTRY_ENVIRONMENT': JSON.stringify(process.env.SENTRY_ENVIRONMENT),
    }),
    //new dotenv(),
  ],

  module: {
    rules: [
      // Use file-loader to handle image assets
      {
        test: /\.(png|jpe?g|gif|woff2?|svg|ico|eot)$/i,
        use: [
          {
            loader: "file-loader",
            options: {
              // Note: `django-webpack-loader`'s `webpack_static` tag does
              //       not yet pick up versioned assets, so we need to
              //       generate image assets without a hash in the
              //       filename.
              // c.f.: https://github.com/owais/django-webpack-loader/issues/138
              name: "[name].[ext]",
            },
          },
        ],
      },

      // Extract compiled SCSS separately from JS
      {
        test: /\.s[ac]ss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          "css-loader",
          "sass-loader",
        ],
      },
    ],
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".scss"],
  }
};
