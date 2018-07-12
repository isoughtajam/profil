const webpack = require('webpack');
const config = {
  entry:  {
    landing: __dirname + '/js/landing/index.jsx',
    app: __dirname + '/js/app/app.entry.jsx',
    admin: __dirname + '/js/admin/admin.entry.jsx',
    links: __dirname + '/js/links/links.entry.jsx'
  },
  output: {
    path: __dirname + '/dist',
    filename: '[name].bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.json$/,
        loader: 'json-loader'
      }
    ]
  }
};

module.exports = config;
