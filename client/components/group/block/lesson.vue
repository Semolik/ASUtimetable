<template>
    <div class="lesson">
        <div class="message" v-if="timerData && isCurrentDay">
            <span> до начала пары </span>
            <span v-if="timerData.hours">
                {{ usePluralize(timerData.hours, ["час", "часа", "часов"]) }}
            </span>
            <span v-if="timerData.minutes">
                {{
                    usePluralize(timerData.minutes, [
                        "минута",
                        "минуты",
                        "минут",
                    ])
                }}
            </span>
        </div>
        <div class="name-line">
            <div class="num">
                {{ lesson.num }}
            </div>
            <div class="lesson-info" v-if="lesson.lesson_info">
                {{ lesson.lesson_info }}
            </div>
            <div class="name">
                {{ lesson.name }}
            </div>
        </div>
        <div class="line">
            <div class="block" v-if="lesson.time && !lesson.is_asynchronous">
                {{ lesson.time?.start }} - {{ lesson.time?.end }}
            </div>
            <div
                :class="[
                    'block lesson-type',
                    { 'is-lecture': lesson.lesson_type === 'лек.' },
                    { 'is-practice': lesson.lesson_type === 'пр.з.' },
                    { 'is-laboratory-work': lesson.lesson_type === 'лаб.' },
                ]"
            >
                {{ lesson.lesson_type }}
            </div>
            <div class="block on-distance" v-if="lesson.on_distance">
                дистанционно
                {{ lesson.is_asynchronous ? "асинхронно" : "синхронно" }}
            </div>

            <div class="block room" v-if="lesson.room">
                {{ lesson.room }}
            </div>
            <div v-if="lesson.lecturer" class="block">
                {{ lesson.lecturer?.name }}
            </div>
        </div>
    </div>
</template>
<script setup>
const { lesson } = defineProps({
    lesson: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.lesson {
    padding: 10px;
    border-radius: 15px;
    background-color: $quaternary-background;
    display: flex;
    flex-direction: column;
    gap: 5px;

    .line {
        display: flex;
        flex-direction: row;
        gap: 5px;
        flex-wrap: wrap;

        .block {
            padding: 2px 15px;
            border-radius: 10px;
            background-color: $senary-background;
            color: $primary-text;
            @include flex-center;
            flex-grow: 1;
            &.room {
                flex-grow: 0;
            }

            &.lesson-type {
                padding: 2px 10px;

                &.is-lecture {
                    background-color: $accent-green;
                }

                &.is-practice,
                &.is-laboratory-work {
                    background-color: $accent-red;
                }
            }
            &:last-child {
                flex-grow: 1;
            }
        }
    }
    .name-line {
        display: flex;
        gap: 5px;
        .num {
            min-width: 30px;
            min-height: 30px;
            border-radius: 10px;
            background-color: $accent-purple;
            @include flex-center;
            color: $primary-text;
        }
        .name {
            background-color: $septenary-background;
            width: 100%;
            border-radius: 10px;
            text-align: center;
            @include flex-center;
            padding: 0px 5px;
        }

        .lesson-info {
            background-color: $accent-purple;
            border-radius: 10px;
            @include flex-center;
            color: $primary-text;
            padding: 0 15px;
        }
    }
}
</style>
