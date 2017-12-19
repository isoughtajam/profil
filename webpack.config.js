const baseDir = __dirname;

module.exports = {
    context: __dirname,
    entry: {
        bundle: [baseDir + "/src/main.js"],
        //test: [baseDir + "/src/utils.js"]
    },
    output: {
        path: baseDir + "/dist",
        filename: "bundle.js"
    },
    module: {
        loaders: [
            { test: /\.css$/, loader: "style!css" },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react']
                }
            }
        ]
    }
};
