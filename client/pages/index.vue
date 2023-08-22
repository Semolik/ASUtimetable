<template>
    <div class="index-page">
        <div class="plus-button" @click="add">
            <Icon name="material-symbols:add-rounded" />
        </div>
    </div>
</template>
<script setup>
const add = () => {};
</script>
<style lang="scss" scoped>
.index-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 10px;
    position: relative;
    height: 100%;

    .plus-button {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: $accent-1;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        svg {
            width: 25px;
            height: 25px;
            color: $secondary-color;
        }
    }
}
</style>
