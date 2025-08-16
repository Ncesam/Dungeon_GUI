import path from 'path';
import webpack from 'webpack';
import {BuildOptions, BuildPaths} from './config/build/types/types';
import ForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin';
import {fileURLToPath} from "url";

function buildMainWebpackConfig(options: BuildOptions): webpack.Configuration {
    const { mode, paths, platform } = options;
    const isDev = mode === 'development';

    return {
        mode: mode ?? 'development',
        entry: {
            main: paths.entry || path.resolve(__dirname, 'src/main.ts'),
            preload: path.resolve(__dirname, 'src/preload.ts'),
        },
        output: {
            filename: '[name].js',
            path: paths.output || path.resolve(__dirname, 'build'),
        },

        target: 'electron-main',

        module: {
            rules: [
                {
                    test: /\.ts$/,
                    exclude: /node_modules/,
                    use: [{
                        loader: 'ts-loader',
                    }],
                },
            ],
        },

        resolve: {
            extensions: ['.ts', '.js']
        },

        plugins: [
            new webpack.DefinePlugin({
                __PLATFORM__: JSON.stringify(platform),
                __ENV__: JSON.stringify(mode),
            }),
            isDev ? new ForkTsCheckerWebpackPlugin({
                typescript: {
                }
            }) : null,
        ].filter(Boolean),

        externals: [
        ],

        devtool: 'source-map',
    };
}


export default () => {
     const paths: BuildPaths = {
        output: path.resolve(__dirname, 'build'),
        entry: path.resolve(__dirname, 'src/', 'main.ts'),
        html: path.resolve(__dirname, 'public', 'index.html'),
        public: path.resolve(__dirname, 'public'),
        src: path.resolve(__dirname, 'src/'),
    }

    return buildMainWebpackConfig({
        port: 3000,
        mode: 'development',
        paths,
        analyzer: false,
        platform: 'desktop'
    });
}