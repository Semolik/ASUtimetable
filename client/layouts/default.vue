<template>
    <head>
        <meta name="theme-color" content="rgb(248, 248, 234)" />
    </head>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <Header />
            <div class="app-content">
                <slot />
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

    .app-content {
        flex-grow: 1;
        padding: 10px;
    }
}
</style>
<script setup>
const fixIssue = (error) => {
    error.value = null;
};
const handleError = (error) => {
    console.error(error);
};
</script>
