<template>
    <BaseContainer>
        <div class="message" v-if="data.message">
            <font-awesome-icon icon="fa-solid fa-triangle-exclamation" />
            <div class="text">{{ data.message }}</div>
        </div>
        <InfoBlock v-bind:showFacultyData="showFacultyData" v-bind:data="data" />
        <div :class="['search', { active: active }]">
            <input type="text" v-model="input" @focus="active = true" @blur="active = false" :placeholder="text"
                ref="search">
            <AnimateInteger class="count" :value="itemsCount" />
        </div>
        <LinksList v-bind:items="items" v-bind:linkbase="linkbase" />
    </BaseContainer>
</template>
<script>
import LinksList from './LinksList.vue';
import InfoBlock from './InfoBlock.vue';
import BaseContainer from './BaseContainer.vue';
import AnimateInteger from './AnimateInteger.vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTriangleExclamation, faArrowsSpin } from '@fortawesome/free-solid-svg-icons';
library.add([faTriangleExclamation, faArrowsSpin]);
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
    components: {
        LinksList,
        FontAwesomeIcon,
        InfoBlock,
        BaseContainer,
        AnimateInteger
    },
    props: {
        text: String,
        data: Object,
        showFacultyData: Boolean,
        linkbase: String,
    },
    data() {
        return {
            active: false,
            input: '',
        }
    },
    mounted() {
        if (this.enableHover) {
            this.$refs.search.focus();
        }
    },
    inject: ['enableHover'],
    computed: {
        items() {
            let text = this.input.toLowerCase();
            if (this.data.items) {
                return this.data.items.filter((item) => {
                    return item.name.toLowerCase().includes(text);
                });
            }
            return []
        },
        itemsCount() {
            return this.items.length
        }
    },
}
</script>
<style scoped lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';

.message {
    background-color: rgba($color: red, $alpha: 0.2);
    width: min(900px, 100%);
    margin: auto;
    padding: 10px;
    border-radius: 10px;
    gap: 10px;
    @include helpers.flex-center;
}

.search {
    margin: auto;
    display: flex;
    width: 100%;
    height: 50px;
    position: relative;
    background-color: var(--color-background-mute);
    border-radius: 10px;
    overflow: hidden;

    .count {
        aspect-ratio: 1;
        height: 100%;
        @include helpers.flex-center;
        color: var(--color-header-text);
    }

    input {
        background-color: var(--color-background-mute);
        border: none;
        padding: 8px 10px;
        color: var(--color-text);
        font-size: 1.1em;
        outline: none;
        width: 100%;

        @include themes.light {
            &::placeholder {
                color: rgba(black, 0.4);
            }
        }
    }

    &.active {
        @include themes.dark {
            --bg: var(--color-background-mute-3);
        }

        @include themes.light {
            --bg: var(--color-background-mute-2);
        }

        background-color: var(--bg);

        input {
            outline: none;
            background-color: var(--bg);
            color: var(--color-text);
        }
    }
}
</style>