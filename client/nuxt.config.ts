// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: ["nuxt-icon", "@pinia/nuxt", "@vueuse/nuxt", "@nuxthq/ui"],
    devtools: { enabled: true },
    ssr: false,
    css: ["@/assets/styles/global.scss"],
    colorMode: {
        preference: "light",
    },
    plugins: ["@/plugins/api", "@/plugins/auto-animate"],
    nitro: {
        devProxy: {
            "/api": {
                target: "http://127.0.0.1:8000",
            },
        },
    },
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: [
                        '@use "@/assets/styles/colors.scss" as *;',
                        '@use "@/assets/styles/breakpoints.scss" as *;',
                        '@use "@/assets/styles/helpers.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
});
