<template>
    <nuxt-link class="item" v-bind="$attrs">
        <slot />
    </nuxt-link>
</template>

<style scoped lang="scss">
.item {
    @include flex-center;
    padding: 20px 10px;
    border-radius: 8px;
    text-align: center;
    text-decoration: none;
    background-color: rgba($color: #000000, $alpha: 0.1);
    transition: all 0.2s ease-in-out;
    @include has-hover {
        transform: translateY(-2px);
        background-color: rgba($color: #000000, $alpha: 0.2);
    }
}
</style>
