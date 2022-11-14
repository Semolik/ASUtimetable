<template>
    <component :is="link ? 'router-link' : 'div'" :to="link"
        :class="['info-block', { active: active }, { hoverable: enableHover }]">
        <slot></slot>
    </component>
</template>
<script>
export default {
    props: {
        active: Boolean,
        link: String
    },
    inject: ['enableHover'],
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/default';
@use '@/assets/styles/helpers';

.info-block {
    border-radius: 20px;
    display: flex;
    justify-content: right;
    gap: 10px;
    text-decoration: none;
    color: var(--color-text);

    .block {
        min-height: 35px;
        overflow: hidden;
        @include default.block;
        @include helpers.vue-skeletor;

        &.no-overflow {
            overflow: visible;
        }
    }

    &.active {
        @at-root {
            a#{&}.hoverable:hover {
                transform: translateY(-2px);

                @include themes.light {
                    box-shadow: var(--main-card-shadow);
                }
            }
        }

        transition: transform .2s,
        background-color .2s,
        box-shadow .5s;
        display: grid;
        gap: 10px;
        grid-template-columns: repeat(3, 1fr);
        padding: 10px;
        @include default.block(--color-background-mute);

        @include themes.dark {
            border: 1px solid var(--color-background-mute-3);
        }

        @include breakpoints.md(true) {
            grid-template-columns: 1fr;
        }

        .block {
            border-radius: 10px;
            text-align: center;
            transition: box-shadow .2s;
            padding: 10px;

            .info-block:not(.active) {
                @include breakpoints.lg {
                    min-height: 100px;
                }
            }
        }
    }
}
</style>