<template>
    <header>
        <nuxt-link to="/" class="header-text">Расписание</nuxt-link>
        <div class="settings-button">
            <Icon name="material-symbols:settings" />
        </div>
    </header>
</template>
<style lang="scss" scoped>
header {
    color: $accent-1;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .header-text {
        font-size: 1.5rem;
        color: $accent-1;
        text-decoration: none;
        font-weight: 500;
    }
    .settings-button {
        background-color: $secondary-color;
        padding: 16px;

        box-shadow: $shadow-1;
        border-radius: 16px;
        svg {
            width: 20px;
            height: 20px;
        }
    }
}
</style>
