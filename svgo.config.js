module.exports = {
    plugins: [
        {
            name: 'preset-default',
            params: {
                overrides: {
                    // Disable viewbox plugin, because we use them
                    removeViewBox: false,
                },
            },
        },
    ],
};
