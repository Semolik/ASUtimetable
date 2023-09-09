<template>
    <div :class="['loading', { darken }]">
        <span v-if="useText">Загрузка...</span>
        <Icon name="svg-spinners:180-ring" v-else />
    </div>
</template>
<script setup>
const { darken, useText } = defineProps({
    darken: {
        type: Boolean,
        default: false,
    },
    useText: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.loading {
    @include flex-center;
    height: 100%;
    width: 100%;
    background-color: $tetriary-background;

    &.darken {
        background-color: $secondary-background;
    }

    svg {
        width: 30px;
        height: 30px;
    }
}
</style>
