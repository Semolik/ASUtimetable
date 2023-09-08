<template>
    <div class="home-group">
        <div class="column">
            <div class="names">
                <div class="name">
                    {{ group.name }}
                </div>
            </div>
            <div
                :class="[
                    'day-of-week',
                    { current: currentDayIndex === selectedDayIndex },
                ]"
            >
                {{ selectedDay.name }}
            </div>
            <div class="dates">
                <div
                    :class="[
                        'date-day',
                        { active: index === selectedDayIndex },
                        { current: day.is_current },
                    ]"
                    v-for="(day, index) in filteredDays"
                    @click="selectedDayIndex = index"
                >
                    <div class="day-number">{{ day.date_text }}</div>
                    <div class="mounth">{{ day.short_name }}</div>
                </div>
            </div>
        </div>
        <nuxt-link
            class="group-link"
            :to="{
                name: 'faculties-faculty_id-groups-group_id',
                params: {
                    faculty_id: group.faculty.id,
                    group_id: group.id,
                },
            }"
        >
            открыть страницу группы
        </nuxt-link>
        <div class="lessons-container">
            <suspense v-if="!isSunday">
                <template #default>
                    <group-block-lessons
                        :group="group"
                        :selected-day-index="selectedDayIndex"
                    />
                </template>
                <template #fallback>
                    <loading />
                </template>
            </suspense>
            <div class="no-lessons" v-else>В воскресенье нет занятий</div>
        </div>
    </div>
</template>
<script setup>
import moment from "moment/min/moment-with-locales";
moment.locale("ru");
const { group } = defineProps({
    group: {
        type: Object,
        required: true,
    },
});

var now_moment = moment();
const now = now_moment.toDate();
var week_start = now_moment.startOf("isoweek").toDate();
week_start.setHours(0, 0, 0, 0);
var week_end = now_moment.endOf("isoweek").toDate();
week_end.setHours(0, 0, 0, 0);
const dateIsEqual = (date1, date2) => {
    return (
        date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear()
    );
};
const days = [];

for (let i = 0; i < 7; i++) {
    const date = new Date(week_start);
    date.setDate(date.getDate() + i);
    const isCurrent = dateIsEqual(date, now);
    const day = {
        date_text: moment(date).format("DD.MM"),
        name: moment(date).format("dddd"),
        short_name: moment(date).format("dd"),
        date: date,
        is_current: isCurrent,
    };
    days.push(day);
}
const selectedDayIndex = ref(days.findIndex((day) => day.is_current));
const currentDayIndex = computed(() => {
    return days.findIndex((day) => day.is_current);
});
const selectedDay = computed(() => days[selectedDayIndex.value]);
const sundayIndex = computed(() =>
    days.findIndex((day) => day.date.getDay() === 0)
);
const filteredDays = computed(() =>
    days.filter((day, index) => index !== sundayIndex.value)
);
const isSunday = computed(() => selectedDay.value.date.getDay() === 0);
</script>
<style lang="scss" scoped>
.home-group {
    padding: 10px;
    background-color: $secondary-background;
    display: grid;
    grid-template-columns: 300px 1fr;
    width: 100%;
    text-decoration: none;
    color: $primary-text;
    border-radius: 25px;
    $gap: 6px;
    $min-block: 30px;
    gap: $gap;

    @include xl(true) {
        grid-template-columns: 1fr;
    }
    .column {
        display: flex;
        flex-direction: column;
        gap: $gap;

        .names {
            display: flex;
            flex-wrap: wrap;
            gap: $gap;
            height: min-content;

            .name {
                padding: 3px 10px;
                flex-grow: 1;
                text-align: center;
                border-radius: 15px;
                @include flex-center;
                min-height: $min-block;
                background-color: $accent-purple;
            }
        }

        .day-of-week {
            background-color: $accent-green;
            padding: 3px;
            min-height: $min-block;
            text-align: center;
            border-radius: 15px;
            @include flex-center;

            &.current {
                background-color: $accent-red;
            }
        }

        .dates {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: $gap;

            @include xl(true) {
                @include lg {
                    grid-template-columns: repeat(6, 1fr);
                    margin-bottom: 10px;
                }
            }

            .date-day {
                cursor: pointer;
                min-height: 71px;
                @include flex-center;
                flex-direction: column;
                flex-grow: 1;
                padding: 10px;
                border-radius: 15px;
                background-color: $quaternary-background;

                &.active {
                    background-color: $accent-green;
                    cursor: auto;
                }

                &.current {
                    background-color: $accent-red-hover;

                    @include has-hover {
                        background-color: $accent-red;
                    }
                    &.active {
                        background-color: $accent-red;
                    }
                }

                &:not(:where(.active, .current)) {
                    @include has-hover {
                        background-color: $senary-background;
                    }
                }

                .day-number {
                    font-size: 1.4em;
                }
            }
        }
    }

    .group-link {
        margin-top: auto;
        text-decoration: none;
        color: $primary-text;
        grid-column: 1;
        padding: 5px;
        text-align: center;
        border-radius: 15px;
        background-color: $qiunary-background;

        @include has-hover {
            background-color: $senary-background;
        }
    }

    .lessons-container {
        @include xl {
            grid-column: 2;
            grid-row: 1 / 3;
        }
        @include xl(true) {
            padding-top: 10px;
        }

        .no-lessons {
            @include flex-center;
            height: 100%;
            background-color: $tetriary-background;
            border-radius: 15px;
        }
    }
}
</style>
