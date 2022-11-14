<template>
    <div :class="['home-group', { hoverable: enableHover }]">
        <div class="column">
            <div class="names">
                <div class="name" v-for="name in groupData.names">{{ name }}</div>
            </div>
            <template v-if="!daysIsEmpty">
                <div :class="['day-of-week', { hidden: selectedDayHidden }, {current: selectedDayIsCurrent}]"
                    v-if="selected_day !== null">
                    {{ selectedDayOfWeek }}
                </div>
                <div class="day-of-week" v-else-if="loading">
                    загрузка
                    <Skeletor />
                </div>
                <div class="dates">
                    <div :class="['date-day', { active: index === selected_day }, { current: index === current_day }]"
                        v-for="(day, index, key) in displayedDays" :key="key" @click="selected_day = index">
                        <template v-if="!loading">
                            <div class="day-number">{{ dayNumber(day) }}</div>
                            <div class="mounth">{{ dayMonth(day) }}</div>
                        </template>
                        <Skeletor v-else />
                    </div>
                </div>
            </template>
        </div>
        <div :class="['message','empty', {error: error}]" v-if="daysIsEmpty">
            <div class="text" v-if="!error">На этой неделе занятий нет</div>
            <div class="text" v-else>{{ errorMessage }}</div>
        </div>
        <div class="error-message" v-if="message">
            <div class="text">{{message}}</div>
        </div>
        <div v-else-if="!loading && !error && selectedDayLessonsEmpty" :class="['message','empty', {error: error}]">
            <div class="text" v-if="!error">В {{selectedDayOfWeekLower}} занятий нет</div>
            <div class="text" v-else>{{ errorMessage }}</div>
        </div>
        <router-link :class="['group-link', {empty: daysIsEmpty}]" :style="{'--row': message? 4: 3}" :to="GroupLink">
            открыть страницу группы
        </router-link>
        <GroupDayInfo :dayData="selectedDayData" v-if="selectedDayData && !selectedDayHidden" />
        <GroupDayInfo v-else-if="loading" loader />
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import 'vue-skeletor/dist/vue-skeletor.css';
import { Skeletor } from 'vue-skeletor';
import handleError from '../composables/errors';
import GroupDayInfo from './GroupDayInfo.vue';
import GroupAddresses from './GroupAddresses.vue';

import { computed } from 'vue';

export default {
    props: {
        groupData: Object,
    },
    components: {
        Skeletor,
        GroupDayInfo,
        GroupAddresses
    },
    data() {
        return {
            days: [],
            error: null,
            loading: false,
            selected_day: null,
            current_day: null,
            last_load_time: null,
            message: null,
        }
    },
    inject: ['enableHover'],
    provide() {
        return {
            loadTime: computed(() => this.last_load_time)
        }
    },
    mounted() {
        this.loading = true;
        HTTP.get('group', { params: { faculty_id: this.groupData.faculty_id, group_id: this.groupData.group_id } })
            .then((response) => {
                this.last_load_time = Date.now();
                const { days, message } = response.data;
                this.days = days;
                this.message = message;
                this.days.forEach((day, index) => {
                    if (day?.day?.current) {
                        this.selected_day = index;
                        this.current_day = index;
                    }
                });
            })
            .catch((error) => {
                this.error = error;
            }).finally(() => {
                this.loading = false;
            });
    },
    methods: {
        dayIsHidden(day) {
            return day?.day?.hide === false
        },
        dayNumber(day) {
            return day?.day?.date.split('.')[0].replace(/^0+/, "");
        },
        dayMonth(day) {
            return day?.day?.month;
        }
    },
    computed: {
        GroupLink() {
            return '/students/' + [this.groupData.faculty_id, this.groupData.group_id].join('/')
        },
        notHiddenDays() {
            return this.days.filter(this.dayIsHidden);
        },
        displayedDays() {
            return this.loading ? Array(6).fill({}) : this.notHiddenDays
        },
        selectedDayData() {
            return this.selected_day !== null ? this.days[this.selected_day] : {};
        },
        selectedDayLessonsEmpty() {
            return this.selectedDayData?.lessons?.length === 0
        },
        selectedDayHidden() {
            return !this.dayIsHidden(this.selectedDayData)
        },
        selectedDayOfWeek() {
            return this.selectedDayData?.day?.day_of_week
        },
        selectedDayOfWeekLower() {
            return this.selectedDayOfWeek ? this.selectedDayOfWeek.toLowerCase() : ''
        },
        selectedDayIsCurrent() {
            return this.selectedDayData?.day?.current === true
        },
        daysIsEmpty() {
            return !this.loading && this.days.length === 0
        },
        errorMessage() {
            return handleError(this.error).message
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/default';
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';
@use '@/assets/styles/animations';
@include animations.list;

.home-group {
    padding: 10px;
    @include default.block(--color-background-mute);
    display: grid;
    grid-template-columns: 300px 1fr;
    width: 100%;
    text-decoration: none;
    color: var(--color-text);
    border-radius: 25px;
    gap: var(--gap);

    @include breakpoints.xl(true) {
        grid-template-columns: 1fr;
    }

    --min-block: 30px;
    --gap: 6px;
    --border-radius: 15px;

    @mixin bg {
        @include themes.light {
            background-color: rgba($color: #000000, $alpha: 0.1);
        }

        @include themes.dark {
            background-color: rgba($color: white, $alpha: 0.07);
        }
    }

    .message.empty,
    .info {
        @include breakpoints.xl {
            grid-row: 1 / 3;
            grid-column: 2;
        }
    }

    .error-message {
        background-color: rgba($color: red, $alpha: 0.2);
        padding: 10px;
        border-radius: 10px;
        gap: 10px;
        @include helpers.flex-center;
        text-align: center;
        .text {
            text-align: center;
        }
    }

    .column {
        display: flex;
        flex-direction: column;
        gap: var(--gap);

        .names {
            display: flex;
            flex-wrap: wrap;
            gap: var(--gap);
            height: min-content;

            .name {
                padding: 3px 10px;
                flex-grow: 1;
                text-align: center;
                border-radius: var(--border-radius);
                @include helpers.flex-center;
                min-height: var(--min-block);
                background-color: var(--purple);
            }
        }

        .day-of-week {
            background-color: var(--green-128);
            padding: 3px;
            min-height: var(--min-block);
            text-align: center;
            border-radius: var(--border-radius);
            @include helpers.flex-center;
            @include helpers.vue-skeletor;

            &.current {
                background-color: var(--red-0);
            }

            &.hidden {
                @include bg;
            }
        }

        .dates {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--gap);

            @include breakpoints.xl(true) {
                @include breakpoints.lg {
                    grid-template-columns: repeat(6, 1fr);
                    margin-bottom: 10px;
                }
            }

            .date-day {
                cursor: pointer;
                min-height: 71px;
                @include helpers.vue-skeletor;
                @include helpers.flex-center;
                flex-direction: column;
                flex-grow: 1;
                padding: 10px;
                border-radius: var(--border-radius);
                @include bg;

                &.active {
                    background-color: var(--green-128);
                    cursor: auto;
                }

                &.current {
                    background-color: var(--red-0-hover);

                    .hoverable &:not(.active):hover,
                    &.active {
                        background-color: var(--red-0);
                    }
                }

                .hoverable &:not(.active):hover {
                    background-color: var(--green-128-hover);
                }

                .day-number {
                    font-size: 1.4em;
                }
            }
        }
    }

    .message {
        @include helpers.flex-center;
        height: 100%;
        width: 100%;
        border: 2px dashed var(--purple);
        border-radius: var(--border-radius);
        overflow: hidden;

        @include breakpoints.xl(true) {
            min-height: 100px;
        }

        @include themes.light {
            border-color: var(--color-background-mute-2);
        }

        &.error {
            position: relative;

            &::after {
                content: '';
                position: absolute;
                inset: 0;
                background-color: var(--red-0);
                z-index: 1;
                opacity: 0.3;
            }
        }

        .text {
            z-index: 2;
            text-align: center;
            font-size: 1.1em;
        }
    }

    .group-link {
        margin-top: auto;
        text-decoration: none;
        color: var(--color-text);
        grid-column: 1;
        padding: 5px;
        text-align: center;
        border-radius: var(--border-radius);

        @include breakpoints.xl(true) {
            grid-row: var(--row);
        }

        @include themes.light {
            background-color: var(--color-background-mute);
        }

        @include themes.dark {
            background-color: var(--color-background-mute-2);
        }

        .hoverable &:hover {
            @include themes.light {
                background-color: var(--color-background-mute-2);
            }

            @include themes.dark {
                background-color: var(--color-background-mute-3);
            }
        }
    }
}
</style>