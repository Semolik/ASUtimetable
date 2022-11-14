<template>
    <InfoBlockBase :active="showFacultyData">
        <div class="updated block" v-if="!runLoading">
            <Transition mode="out-in">
                <div class="text" v-if="!loading">обновлено {{  data.last_updated  }}</div>
                <div class="text" v-else>загрузка...</div>
            </Transition>
        </div>
        <div class="updated block" v-else>
            <Skeletor />
        </div>
        <template v-if="showFacultyData">
            <template v-if="!runLoading">
                <div class="name item block" v-if="data.name">{{  data.name  }}</div>
                <div class="blocks" v-if="!isGroupView">
                    <div class="type item block" v-if="data.type">{{  data.type  }}</div>
                    <div class="location item block" v-if="data.location">{{  data.location  }}</div>
                    <div class="address item block" v-if="data.address">{{  data.address  }}</div>
                </div>
            </template>
            <template v-else>
                <div class="name item block">
                    <Skeletor />
                </div>
                <div class="blocks" v-if="!isGroupView">
                    <div class="type item block">
                        <Skeletor />
                    </div>
                    <div class="location item block">
                        <Skeletor />
                    </div>
                    <div class="address item block">
                        <Skeletor />
                    </div>
                </div>
            </template>
        </template>
    </InfoBlockBase>
</template>

<script>
import { Skeletor } from 'vue-skeletor';
import 'vue-skeletor/dist/vue-skeletor.css';
import InfoBlockBase from './InfoBlockBase.vue';

export default {
    components: {
        Skeletor,
        InfoBlockBase,
    },
    computed: {
        runLoading() {
            return this.disableLoading ? false : this.loading
        }
    },
    props: {
        showFacultyData: Boolean,
        data: Object,
        isGroupView: Boolean
    },
    inject: ['enableHover', 'loading', 'disableLoading'],

}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';

.info-block {
    &.active {
        .name {
            @include breakpoints.md {
                grid-column: 1 / 3;
                grid-row: 1;
            }
        }

        .item {
            width: 100%;
            height: 100%;
            @include helpers.flex-center;
        }

        .updated {
            min-height: 42px;
            width: 100%;

            @include breakpoints.md {
                grid-column: 3;
            }
        }

        .blocks {
            display: flex;
            gap: 10px;
            grid-column: 1 / -1;

            @include breakpoints.md(true) {
                flex-direction: column;
            }

            .item {
                border-radius: 10px;
                padding: 10px;
            }
        }
    }

    .updated {
        @include helpers.flex-center;
        min-width: 200px;
        gap: 10px;
        border-radius: 10px;
        padding: 5px 10px;
        text-align: center;

        @include breakpoints.md(true) {
            width: 100%;
        }

        .text {
            height: min-content;
        }

        .v-enter-active,
        .v-leave-active {
            transition: opacity 0.3s ease;
        }

        .v-enter-from,
        .v-leave-to {
            opacity: 0;
        }
    }
}
</style>
