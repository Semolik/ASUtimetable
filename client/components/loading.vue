<template>
    <div class="loading">загрузка...</div>
</template>
<style lang="scss" scoped>
.loading {
    @include flex-center;
    height: 100%;
    width: 100%;
    background-color: $tetriary-background;

    svg {
        width: 100px;
        height: 100px;
    }
}
</style>
