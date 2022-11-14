<template>
    <TransitionGroup :css="false" name="list" tag="div" :class="['items', { hoverable: enableHover }]"
        v-if="!loading && items">
        <router-link :to="linkbase + item.id" class="item" v-for="item in items" :key="item.name">{{ item.name }}
        </router-link>
    </TransitionGroup>
    <div class="items" v-else>
        <div class="item" v-for="_ in Array(20).fill({})">
            <Skeletor />
        </div>
    </div>
</template>

<script>
import 'vue-skeletor/dist/vue-skeletor.css';
import { Skeletor } from 'vue-skeletor';
export default {
    props: {
        items: Array,
        linkbase: String
    },
    components: { Skeletor },
    inject: ['enableHover', 'loading'],

}
</script>

<style scoped lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/default';
@use '@/assets/styles/helpers';
@use '@/assets/styles/animations';

@include animations.list;

.items {
    display: grid;
    gap: 15px;
    width: min(1400px, 100%);
    margin: auto;

    @include breakpoints.xs {
        grid-template-columns: 1fr;
    }

    @include breakpoints.sm {
        grid-template-columns: repeat(2, 1fr);
    }

    @include breakpoints.md {
        grid-template-columns: repeat(3, 1fr);
    }

    @include breakpoints.lg {
        grid-template-columns: repeat(4, 1fr);
    }

    @include breakpoints.xl {
        grid-template-columns: repeat(5, 1fr);
    }

    &.hoverable {
        .item:hover {
            transform: translateY(-2px);
            @include default.block;
            box-shadow: var(--main-card-shadow);
        }
    }

    .item {
        width: 100%;
        padding: 15px;
        min-height: 50px;

        @include breakpoints.lg {
            padding: 20px;
            min-height: 60px;
        }

        text-decoration: none;
        color: var(--color-text);
        display: grid;
        place-content: center;
        border-radius: 10px;
        text-align: center;
        transition: transform .2s,
        background-color .2s,
        box-shadow .5s;
        overflow: hidden;
        @include default.block(--color-background-mute);
        @include helpers.vue-skeletor;
    }
}
</style>