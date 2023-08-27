<template>
    <div class="items" v-auto-animate>
        <slot />
    </div>
</template>
<style scoped lang="scss">
.items {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;
}
</style>
