const webpack = require('webpack');
const config = {
  mode: 'production',
  entry:  {
    landing: __dirname + '/js/landing/index.jsx',
    app: __dirname + '/js/app/app.entry.jsx',
    admin: __dirname + '/js/admin/admin.entry.jsx',
    links: __dirname + '/js/links/links.entry.jsx',
    search: __dirname + '/js/search/search.entry.jsx'
  },
  output: {
    path: __dirname + '/dist',
    filename: '[name].bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.json']
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      }
    ]
  }
};

module.exports = config;
