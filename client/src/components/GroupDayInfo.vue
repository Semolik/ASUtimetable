<template>
    <div class="info">
        <template v-if="!lessonsEmpty">
            <GroupDayInfoLessonsItem @get-data="$emit('get-data', $event)" :lesson="lesson"
                v-for="lesson in lessons" />
        </template>
        <div v-else :class="['lessons-empty', { loading: loader }]">
            <template v-if="loader">
                <span>загрузка</span>
            </template>
            <span v-else>нет занятий</span>
        </div>
    </div>
</template>
<script>
import DeclinationByNumber from './DeclinationByNumber.vue';
import GroupDayInfoLessonsItem from './GroupDayInfoItem.vue';
import { computed } from 'vue';
export default {
    props: {
        dayData: Object,
        loader: Boolean,
    },
    components: {
        DeclinationByNumber,
        GroupDayInfoLessonsItem,
    },

    computed: {
        lessons() {
            return this.dayData?.lessons || []
        },
        lessonsEmpty() {
            return this.lessons.length === 0
        },
        isCurrentDay() {
            return this.dayData?.day.current === true
        }
    },
    provide() {
        return {
            isCurrentDay: computed(() => this.isCurrentDay)
        }
    }
};
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';
@use '@/assets/styles/default';
@use '@/assets/styles/breakpoints';

.info {
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    gap: 5px;

    .lessons-empty {
        width: 100%;
        height: 100%;
        @include helpers.flex-center;
        border: 2px dashed transparent;
        min-height: 50px;
        border-radius: 20px;
        font-size: 1.1em;
        border-color: var(--purple);

        .home-group & {
            border-radius: var(--border-radius);
        }

        @include breakpoints.md(true) {
            min-height: 100px;
        }

        @include themes.light {
            border-color: var(--color-background-mute-2);
        }
    }

    .item {
        min-height: 37px;
        border-radius: 15px;
        height: min-content;

        .home-group & {
            border-radius: var(--border-radius);
        }

        width: 100%;
        @include helpers.flex-center;
        padding: 5px;
        flex-wrap: wrap;
        gap: 5px;
        text-align: center;

        --text-block-light-color: var(--color-background-mute-3);
        --text-block-dark-color: var(--color-background-mute);

        &.on-distance {
            --text-block-light-color: var(--nav-toggle-color);
            --text-block-dark-color: var(--purple-1);
        }

        &.full-time {
            --text-block-light-color: #ff9ec3;
            --text-block-dark-color: #E6377A;
        }

        @include themes.light {
            background-color: var(--text-block-light-color);

            &.multiple {
                background-color: transparent;
                border: 1px solid var(--text-block-light-color);
            }
        }

        @include themes.dark {
            background-color: var(--text-block-dark-color);

            &.multiple {
                background-color: transparent;
                border: 1px solid var(--text-block-dark-color);
            }
        }

        .text {
            padding: 0px 5px;
            flex-grow: 1;

            &.highlight {
                @include themes.light {
                    background-color: var(--text-block-light-color);
                }

                @include themes.dark {
                    background-color: var(--text-block-dark-color);
                }

                text-align: center;
                padding: 2px 10px;
                border-radius: 10px;

                .home-group & {
                    border-radius: calc(var(--border-radius) - 5px);
                }

                height: min-content;
            }
        }
    }
}
</style>