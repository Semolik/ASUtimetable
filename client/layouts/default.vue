<template>
    <head>
        <meta name="theme-color" content="rgb(248, 248, 234)" />
    </head>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <Header />
            <div :class="['app-content', { loading: loading }]">
                <slot />
                <transition class="loading" mode="out-in">
                    <Loading darken v-if="loading" />
                </transition>
            </div>
        </div>
        <template #error="{ error }">
            <Error :error="error" @clearError="fixIssue(error)" />
        </template>
    </NuxtErrorBoundary>
</template>
<style lang="scss" scoped>
.default-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-width: 1400px;
    margin: 0 auto;
    .app-content {
        flex-grow: 1;
        padding: 10px;

        isolation: isolate;
        .v-enter-active,
        .v-leave-active {
            transition: opacity 0.5s ease;
        }

        .v-enter-from,
        .v-leave-to {
            opacity: 0;
        }

        .loading {
            position: absolute;
            inset: 0;
        }

        &.loading {
            overflow: hidden;
        }
    }
}
</style>
<script setup>
const loading = useLoading();
const fixIssue = (error) => {
    error.value = null;
};
const handleError = (error) => {
    console.error(error);
};
</script>
