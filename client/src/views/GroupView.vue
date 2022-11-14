<template>
    <BaseContainer>
        <div class="group-header-wrapper">
            <template v-if="(disableLoading ? true : !loading) && data.header_text">
                <div class="group-header-text">
                    <div class="text">
                        {{ data.header_text }}
                    </div>
                </div>
                <div :class="['button', { active: liked }]" @click="handleClickLikeButton">
                    <FontAwesomeIcon icon="fa-heart" />
                </div>
            </template>
            <Skeletor v-if="loading && !disableLoading" />
        </div>
        <InfoBlock :data="data" showFacultyData isGroupView :link="'/students/' + faculty_id" />
        <div :class="['controls', { hoverable: enableHover }]">
            <div class="button" @click="toWeek(false)">прошлая неделя</div>
            <div class="date">
                <DatePicker @update:modelValue="handleDateChanges" @popoverDidShow="popoverShowed = true"
                    @popoverWillHide="popoverShowed = false" mode="range" v-model="range" ref="calendar"
                    class="calendar" :is-dark="themeName === 'dark'" :attributes='attrs' is-range is-expanded>
                    <template v-slot="{ inputValue, togglePopover }" v-if="breakpoint">
                        <div class="button" :tabindex="0"
                            @click="togglePopover({ placement: 'bottom', transition: 'fade', showDelay: 0, hideDelay: 0 })">
                            <template v-if="dateSelected">
                                {{ inputValue.start }} - {{ inputValue.end }}
                            </template>
                            <div v-else>выбрать даты</div>
                        </div>
                    </template>
                </DatePicker>
                <div :class="['button', 'reset', { disabled: !dateSelected }]" @click="resetDateRange">
                    <div class="text">сбросить даты</div>
                    <FontAwesomeIcon icon="fa-trash" />
                </div>
            </div>
            <div class="button" @click="toWeek(true)">
                следущая неделя
            </div>
        </div>
        <div class="days-line" />
        <div class="error-message" v-if="data.message">
            <font-awesome-icon icon="fa-solid fa-triangle-exclamation" />
            <div class="text">{{ data.message }}</div>
        </div>
        <GroupAddresses :data="data" />
        <TransitionGroup :css="false" name="list" tag="div" class="days">
            <template v-if="!daysIsEmpty">
                <GroupDay @get-data="getData" :dayData="day_data" v-for="(day_data, key) in notHiddenDays" :key="key" />
            </template>
            <div v-else-if="!loading" class="message">Занятий на выбранном диапазоне дат нет</div>
            <Skeletor v-else />
        </TransitionGroup>
    </BaseContainer>
</template>

<script>
import BaseContainer from '../components/BaseContainer.vue';
import InfoBlock from '../components/InfoBlock.vue';
import 'v-calendar/dist/style.css';
import { DatePicker } from 'v-calendar';
import { HTTP } from '../http-common.vue';
import { useThemeStore } from '../stores/theme';
import { useGroupsStore } from '../stores/groups';
import { storeToRefs } from 'pinia';
import moment from 'moment';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTrash, faHeart, faAngleUp, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import 'vue-skeletor/dist/vue-skeletor.css';
import { Skeletor } from 'vue-skeletor';
import GroupDay from '../components/GroupDay.vue';
import GroupAddresses from '../components/GroupAddresses.vue';
import DeclinationByNumber from '../components/DeclinationByNumber.vue';
library.add([faTrash, faHeart, faAngleUp, faTriangleExclamation]);

export default {
    setup() {
        const { themeName } = storeToRefs(useThemeStore());
        const { containsGroup, addGroup, removeGroup } = useGroupsStore();
        return {
            themeName,
            containsGroup,
            addGroup,
            removeGroup
        }
    },
    inject: ['windowWidth', 'enableHover', 'loading'],
    components: {
        BaseContainer,
        InfoBlock,
        DatePicker,
        FontAwesomeIcon,
        Skeletor,
        GroupDay,
        GroupAddresses,
        DeclinationByNumber
    },
    provide() {
        return {
            disableLoading: computed(() => this.disableLoading),
            loadTime: computed(() => this.last_load_time),
        }
    },
    data() {
        var params = this.$router.currentRoute.value.params;
        var now_moment = moment();
        var week_start = now_moment.startOf('isoweek').toDate();
        week_start.setHours(0, 0, 0, 0);
        var week_end = now_moment.endOf('isoweek').toDate();
        week_end.setHours(0, 0, 0, 0);
        return {
            faculty_id: params.faculty_id,
            group_id: params.group_id,
            data: {},
            week_start: week_start,
            week_end: week_end,
            range: {
                start: week_start,
                end: week_end
            },
            attrs: [
                {
                    key: 'today',
                    highlight: 'red',
                    dates: new Date(),
                },
            ],
            popoverShowed: false,
            disableLoading: false,
            liked: false,
            last_load_time: null,
        }
    },
    computed: {
        dateSelected() {
            return this.datesIsSelected();
        },
        breakpoint() {
            return this.windowWidth > 768
        },
        days() {
            return this.data?.days || []
        },
        notHiddenDays() {
            return this.days.filter(day => day?.day?.hide !== true)
        },
        daysIsEmpty() {
            return this.days.length === 0
        },
        allLessons() {
            return [].concat.apply([], this.days.map(day => day.lessons));
        },
        allLessonsNames() {
            return [... new Set(this.allLessons.map(lesson => lesson?.name))].filter(Boolean)
        },
        allLessonsLecturers() {
            return [... new Set(this.allLessons.map(lesson => {
                return lesson?.lecturer.name
            }))].filter(Boolean)
        },
        lecturesCount() {
            return this.countOfLessonType('is_lecture', true)
        },
        practicesCount() {
            return this.countOfLessonType('is_practice', true)
        },
        laboratoryWorksCount() {
            return this.countOfLessonType('is_laboratory_work', true)
        }
    },
    mounted() {
        if (isNaN(this.faculty_id) || isNaN(this.group_id)) {
            this.$router.push('/404');
        }
        this.liked = this.isLikedGroup();
        this.getData();
    },
    methods: {
        countOfLessonType(key, value) {
            return this.allLessons.filter(lesson => lesson?.type ? lesson?.type[key] === value : false).length
        },
        datesIsSelected() {
            return !(this.datesEquals(this.week_end, this.range.end) &&
                this.datesEquals(this.week_start, this.range.start))
        },
        handleDateChanges() {
            if (this.popoverShowed || !this.breakpoint) {
                this.$refs.calendar.focusDate(this.$refs.calendar.value_.start)
            }
            this.getData();
        },
        toWeek(next = false) {
            let start = moment(this.range.start).add(next ? 7 : -7, 'days').startOf('isoweek').toDate()
            this.$refs.calendar.updateValue({
                start: start,
                end: moment(start).add(6, 'days').toDate()
            });
        },
        datesEquals(date1, date2) {
            return moment(date1).isSame(date2)
        },
        resetDateRange() {
            this.$refs.calendar.updateValue({
                start: this.week_start,
                end: this.week_end,
            })
        },
        formatDate(date) {
            return moment(date).format('YYYYMMDD');
        },
        getData() {
            this.$emit('loading', true);
            let range = this.$refs.calendar.value_;
            let params = {
                faculty_id: this.faculty_id,
                group_id: this.group_id,
                date_start: this.formatDate(range.start),
                date_end: this.formatDate(range.end),
            };
            this.last_load_time = Date.now();
            HTTP.get('group', { params: params })
                .then((response) => {
                    if (response.status == 404) {
                        this.$router.push('/404');
                    }
                    this.data = response.data;
                    this.disableLoading = true;
                })
                .catch((error) => {
                    this.$emit('request_error', error);
                }).finally(() => {
                    this.$emit('loading', false);
                });
        },
        isLikedGroup() {
            return this.containsGroup(this.faculty_id, this.group_id)
        },
        handleClickLikeButton() {
            this.liked = this.isLikedGroup();
            if (this.liked) {
                this.removeGroup(this.faculty_id, this.group_id);
            } else {
                var names = [this.data?.name, this.data?.group_name].filter(Boolean);
                this.addGroup(this.faculty_id, this.group_id, this.data?.group_name ? names : [this.data?.header_text])
            }
            this.liked = !this.liked;
        }
    }
}
</script>
<style scoped lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/default';
@use '@/assets/styles/helpers';
@use '@/assets/styles/animations';
@include animations.list;

.group-header-wrapper {
    min-height: 50px;
    border-radius: 15px;
    padding: 5px;
    @include helpers.flex-center;
    @include helpers.vue-skeletor;

    @include themes.dark {
        background-color: var(--color-background-mute-2);
    }

    @include themes.light {
        background-color: var(--main-card-border);
    }

    .group-header-text {
        flex-grow: 1;

        .text {
            font-size: large;
            text-align: center;
        }
    }

    .button {
        height: 40px;
        width: 40px;

        border-radius: 10px;
        padding: 5px;
        @include helpers.flex-center;
        transition: background-color .4s;

        @include themes.light {
            background-color: rgba(0, 0, 0, 0.15);

            &.active {
                svg {
                    color: #FF2400
                }
            }
        }

        @include themes.dark {
            background-color: var(--nav-toggle-color);

            &.active {
                background-color: #FF2400;
            }
        }

        svg {
            transition: color .2s;
            color: black;
            width: 100%;
            height: 100%;
        }
    }
}

.controls {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;

    @include breakpoints.md(true) {
        grid-template-columns: 1fr;
    }

    .button {
        border-radius: 15px;
        cursor: pointer;
        text-align: center;
        padding: 10px;
        transition: box-shadow .5s, background-color .2s;
        @include default.block;

        .hoverable &:hover {
            @include themes.dark {
                background-color: var(--color-background-mute-3);
            }

            @include themes.light {
                box-shadow: var(--main-card-shadow);
            }
        }
    }

    .date {
        display: grid;

        .calendar {
            width: 100%;

            .button {
                height: 100%;
            }
        }

        @include breakpoints.md {
            grid-template-columns: 1fr min-content;
        }

        @include breakpoints.md(true) {
            flex-direction: column;
        }

        .reset {
            transition: max-height .2s, max-width .2s, padding .2s, margin-left .2s, margin-top .2s, opacity .2s, box-shadow .5s, background-color .2s;
            opacity: 1;

            @include breakpoints.md {
                height: 100%;
                max-width: 50px;
                margin-left: 5px;
                aspect-ratio: 1;
                @include helpers.flex-center;

                .text {
                    display: none;
                }

                svg {
                    width: 18px;
                    height: 18px;
                }
            }

            @include breakpoints.md(true) {
                max-height: 100px;
                margin-top: 10px;

                svg {
                    display: none;
                }
            }

            &.disabled {
                opacity: 0;
                padding: 0;

                @include breakpoints.md {
                    margin: 0;
                    max-width: 0;
                }

                @include breakpoints.md(true) {
                    margin-top: 0;
                    max-height: 0;
                }
            }
        }
    }
}

.error-message {
    background-color: rgba($color: red, $alpha: 0.2);
    padding: 10px;
    border-radius: 15px;
    gap: 10px;
    @include helpers.flex-center;
    text-align: center;
}

.days-line {
    @include breakpoints.md {
        display: none;
    }

    position: relative;

    &::after,
    &::before {
        content: '';
        position: absolute;
        bottom: 0;
        width: 100%;
    }

    &::after {
        left: -100%;
    }

    &::before {
        right: -100%;
    }

    &,
    &::after,
    &::before {
        border-top: 1px solid var(--color-background-mute-2);
    }
}

.days {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .vue-skeletor {
        flex-grow: 1;
        grid-column: 1 / -1;
        min-height: 40px;
    }

    .message {
        @include helpers.flex-center;
        flex-grow: 1;
        grid-column: 1 / -1;
        min-height: 100px;
        border: 2px dashed var(--color-text);
        border-radius: var(--border-radius);
        overflow: hidden;
        border-radius: 15px;
    }

    @include breakpoints.md {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
    }

    @include breakpoints.lg {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>
