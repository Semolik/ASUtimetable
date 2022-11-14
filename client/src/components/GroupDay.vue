<template>
    <div :class="['day', { current: dayData.day.current }]">
        <div class="headline">
            <div class="day-of-week">{{ dayData.day.day_of_week }}</div>
            <div class="date">{{ dayData.day.date }}</div>
        </div>
        <GroupDayInfo v-on:updateFilter="$emit('updateFilter', $event)" v-on:get-data="$emit('get-data', $event)" :dayData="dayData" />
    </div>
</template>
<script>

import GroupDayInfo from './GroupDayInfo.vue';
export default {
    props: {
        dayData: Object
    },
    components: { GroupDayInfo }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';
@use '@/assets/styles/default';
@use '@/assets/styles/breakpoints';

.day {
    padding: 10px;
    border-radius: 25px;
    @include default.block(--color-background-mute);
    display: grid;
    grid-template-rows: min-content 1fr;
    gap: 10px;

    &.current {
        .headline .date {
            @include themes.light {
                background-color: var(--nav-toggle-color);
            }

            @include themes.dark {
                background-color: var(--purple-1);
            }
        }
    }

    .headline {
        @include helpers.flex-center;
        margin-bottom: 5px;

        .day-of-week {
            flex-grow: 1;
            font-size: larger;
        }

        .date {
            padding: 2px 7px;
            border-radius: 15px;
            height: min-content;
        }
    }
}
</style>
