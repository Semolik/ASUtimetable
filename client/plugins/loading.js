export default defineNuxtPlugin((nuxtApp) => {
    const loading = useLoading();
    nuxtApp.hook("page:start", () => {
        loading.value = true;
        console.log("loading");
    });
    nuxtApp.hook("page:finish", () => {
        loading.value = false;
        console.log("finish");
    });
});
