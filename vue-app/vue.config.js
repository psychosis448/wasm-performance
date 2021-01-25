const path = require('path')
const WasmPackPlugin = require('@wasm-tool/wasm-pack-plugin')

module.exports = {
    outputDir: "../node-server/public",
    chainWebpack: config => {
        // worker-loader
        config.module
            .rule('worker')
            .test(/\.worker\.(c|m)?js$/i)
            .use('worker-loader')
            .loader('worker-loader')
            .options({ filename: '[contenthash].worker.js', })
            .end()

        // don't mush workers together
        config.module
            .rule('js')
            .exclude
            .add(/\.worker\.(c|m)?js$/i)

        // wasm-pack loader
        config.plugin('wasm-pack')
            .use(WasmPackPlugin, [{
                crateDirectory: path.resolve(__dirname, '../rust-lib'),
                outDir: "../vue-app/wasm-pkg"
            }])
    }
}
