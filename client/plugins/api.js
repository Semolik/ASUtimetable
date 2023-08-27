import { OpenAPI } from "@/client";
export default defineNuxtPlugin((nuxtApp) => {
    OpenAPI.BASE = "/api";
});
