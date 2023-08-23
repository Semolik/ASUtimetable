// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: ["nuxt-icon", "@pinia/nuxt", "@vueuse/nuxt"],
    devtools: { enabled: true },
    ssr: false,
    css: ["@/assets/styles/global.scss"],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: [
                        '@use "@/assets/styles/colors.scss" as *;',
                        '@use "@/assets/styles/breakpoints.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
});
