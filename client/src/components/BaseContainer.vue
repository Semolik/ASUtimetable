<template>
    <div class="base-container">
        <slot></slot>
    </div>
</template>

<style>
.base-container {
    width: min(1400px, 100%);
    display: grid;
    gap: 15px;
}
</style>