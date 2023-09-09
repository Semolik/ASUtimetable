// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: ["nuxt-icon", "@pinia/nuxt", "@vueuse/nuxt", "@nuxthq/ui"],
    devtools: { enabled: true },
    ssr: false,
    css: ["v-calendar/style.css", "@/assets/styles/global.scss"],
    experimental: {
        typedPages: true,
    },
    colorMode: {
        preference: "light",
    },
    plugins: ["@/plugins/api", "@/plugins/auto-animate", "@/plugins/loading"],
    nitro: {
        devProxy: {
            "/api": {
                target: "http://127.0.0.1:8000",
            },
        },
    },
    app: {
        head: {
            meta: [
                {
                    name: "theme-color",
                    content: "#181818",
                },
            ],
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
                        '@use "@/assets/styles/animations.scss" as *;',
                        '@use "@/assets/styles/themes.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
});
