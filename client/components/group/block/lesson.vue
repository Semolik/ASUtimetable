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
        <div class="name">{{ lesson.name }}</div>
        <div class="line">
            <div class="block" v-if="time && !(isOnDistance && isAsyncLesson)">
                {{ time }}
            </div>
            <div class="block on-distance" v-if="lesson.on_distance">
                дистанционно
            </div>
            <div class="block on-distance" v-if="lesson.is_asynchronous">
                асинхронно
            </div>
            <div class="block is-lecture" v-if="lesson.lesson_type === 'лек.'">
                лекция
            </div>
            <div
                class="block is-practice"
                v-if="lesson.lesson_type === 'пр.з.'"
            >
                практическое занятие
            </div>
            <div
                class="block is-laboratory-work"
                v-if="lesson.lesson_type === 'лаб.'"
            >
                лабораторная работа
            </div>
            <div class="block audience">
                <div class="audience-number">аудитория {{ lesson.room }}</div>
                <div class="location" v-if="audienceLocation">
                    {{ audienceLocation }}
                </div>
            </div>
            <div v-if="lecturer" :to="lecturerLink" class="block">
                {{ lecturerText }}
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
}
</style>
