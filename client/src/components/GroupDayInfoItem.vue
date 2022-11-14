<template>
    <div :class="['lesson', { hoverabe: !enableHover }]">
        <div class="message" v-if="timerData && isCurrentDay">
            <span>
                до
                <span v-if="!isNowLesson">начала</span>
                <span v-else>конца</span>
                пары
            </span>
            <DeclinationByNumber v-if="timerData.hours" :number="timerData.hours" :words="['час', 'часа', 'часов']" />
            <DeclinationByNumber v-if="timerData.minutes + 1" :number="timerData.minutes + 1"
                :words="['минута', 'минуты', 'минут']" />
        </div>
        <div class="name">{{ lesson.name }}</div>
        <div class="line">
            <div class="block" v-if="time && !(isOnDistance && isAsyncLesson)">{{ time }}</div>
            <div class="block on-distance" v-if="isOnDistance">дистанционно</div>
            <div class="block on-distance" v-if="isAsyncLesson">асинхронно</div>
            <div class="block lesson-type-name" v-if="!lessonTypeFound && lessonTypeName">{{ lessonTypeName }}</div>
            <div :class="['block', 'is-lecture', { filter: filterByLectures }]" v-if="isLecture">
                лекция
            </div>
            <div :class="['block', 'is-practice', { filter: filterByPractices }]" v-if="isPractice">
                практическое занятие
            </div>
            <div :class="['block', 'is-laboratory-work', { filter: filterByLaboratoryWorks }]" v-if="isLaboratoryWork">
                лабораторная работа</div>
            <div class="block audience" v-if="audienceNumbers">
                <div class="audience-number">аудитория {{ audienceNumbers }}</div>
                <div class="location" v-if="audienceLocation">{{ audienceLocation }}</div>
            </div>
            <div v-if="lecturer" :to="lecturerLink" class="block">{{ lecturerText }}</div>
        </div>
    </div>
</template>
<script>
import DeclinationByNumber from './DeclinationByNumber.vue';

export default {
    props: {
        lesson: Object
    },
    data() {
        return {
            timerTime: null,
            stop_timer: false,
            requested: false,
        };
    },
    mounted() {
        this.setTimer();
    },
    inject: ["enableHover", "loadTime", "nowTime", "isCurrentDay"],
    computed: {
        isNowLesson() {
            return this.lesson?.time?.now === true;
        },
        timerData() {
            if (!this.timerTime) return;
            let all_seconds = this.timerTime - Math.floor(this.nowTime / 1000); // для текущей пары
            let hours = Math.floor(all_seconds / 3600); // get hours
            let minutes = Math.floor((all_seconds - (hours * 3600)) / 60); // get minutes
            let hours_ = (hours > 0 ? hours : null);
            let minutes_ = (minutes > 0 ? minutes : null);

            if (all_seconds > 1) {
                if (all_seconds < 60) {
                    return { hours: null, minutes: 0 };
                }
                return { hours: hours_, minutes: minutes_ };
            } else if (!this.requested) {
                this.$emit('get-data');
                this.requested = true;
                this.setTimer();
            }
        },
        audienceNumbers() {
            return this.lesson?.audience?.number?.join(" / ");
        },
        audienceLocation() {
            return this.lesson?.audience?.location;
        },
        isOnDistance() {
            return this.lessonType.on_distance === true;
        },
        isAsyncLesson() {
            return this.lessonType.is_async === true;
        },
        lessonType() {
            return this.lesson?.type || {};
        },
        lessonTypeName() {
            return this.lessonType.name;
        },
        isPractice() {
            return this.lessonType.is_practice === true;
        },
        isLaboratoryWork() {
            return this.lessonType.is_laboratory_work === true;
        },
        isLecture() {
            return this.lessonType.is_lecture === true;
        },
        lessonTypeFound() {
            return this.isPractice || this.isLecture || this.isLaboratoryWork;
        },
        time() {
            let time = this.lesson?.time;
            if (!time)
                return;
            return [time.start, time.stop].join(" - ");
        },
        lecturer() {
            return this.lesson?.lecturer;
        },
        lecturerLink() {
            return this.lecturer ? "/lecturers/" + [this.lecturer.department_id, this.lecturer.faculty_id, this.lecturer.id].join("/") : "";
        },
        lecturerText() {
            return this.lecturer ? [this.lecturer.type, this.lecturer.name].filter(Boolean).join(" ") : "";
        }
    },
    methods: {
        setTimer() {
            let timer = this.lesson?.time?.timer;
            if (!timer)
                return;
            if (!this.loadTime)
                return;
            this.timerTime = Math.floor(this.loadTime / 1000) + timer;
        },
    },
    components: { DeclinationByNumber }
}
</script>
<style lang="scss">
@use '@/assets/styles/default';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';

.lesson {
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 5px;
    --radius: 10px;
    border-radius: calc(var(--radius) + 5px);
    @include default.block;

    @include themes.light {
        background-color: var(--main-card-border);
    }

    .home-group & {
        border-radius: var(--border-radius);
    }

    .line {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;

        .block {
            text-decoration: none;
            color: var(--color-text);
            padding: 3px 20px;
            flex-grow: 1;
            border-radius: var(--radius);
            text-align: center;

            &.filter {
                color: var(--color-text-rev) !important;
                background-color: var(--color-text) !important;
            }

            @include helpers.flex-center;

            @include themes.light {
                background-color: rgba($color: #000000, $alpha: 0.1);
            }

            @include themes.dark {
                background-color: rgba($color: white, $alpha: 0.07);
            }

            &.is-lecture {
                background-color: var(--green-128);
            }

            &.is-laboratory-work,
            &.is-practice {
                background-color: var(--color-36);
            }

            &.audience {
                padding: 0;
                overflow: hidden;

                .audience-number {
                    flex-grow: 1;
                    padding: 3px 10px;
                }

                .location {
                    @include helpers.flex-center;
                    height: 100%;
                    padding: 0px 10px;
                    background-color: var(--red-0);
                }
            }
        }
    }

    .message,
    .name {
        background-color: var(--color-216);
        border-radius: var(--radius);
        padding: 3px 10px;
        text-align: center;

        &.message {
            background-color: var(--red-0);
            gap: 3px;
            @include helpers.flex-center;
        }
    }
}
</style>