<template>
    <header>
        <nuxt-link to="/" class="settings-button">
            <Icon name="material-symbols:home" />
        </nuxt-link>
        <div class="header-text" id="header-text">{{ headerText }}</div>
        <div
            class="settings-button"
            @click="settingsModalActive = !settingsModalActive"
        >
            <Icon name="material-symbols:settings" />
        </div>

        <Modal v-model:active="settingsModalActive" :min-height="500">
            <template #content>asdas </template>
        </Modal>
    </header>
</template>
<script setup>
const settingsModalActive = ref(false);
</script>
<style lang="scss" scoped>
header {
    padding: 10px;
    padding-bottom: 0px;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    .header-text {
        font-size: 1.2rem;

        text-decoration: none;
        font-weight: 500;
        width: 100%;
        @include flex-center;
        height: 100%;
    }
    .settings-button {
        padding: 16px;
        cursor: pointer;
        background-color: $secondary-background;
        border-radius: 16px;
        height: min-content;
        svg {
            width: 25px;
            height: 25px;
        }
    }
}
</style>
