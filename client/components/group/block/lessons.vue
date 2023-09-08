<template>
    <div class="lessons">
        <GroupBlockLesson
            v-for="lesson in group.days[selectedDayIndex].lessons"
            :lesson="lesson"
        />
    </div>
</template>

<script setup>
import { DefaultService } from "@/client";
const props = defineProps({
    group: {
        type: Object,
        required: true,
    },
    selectedDayIndex: {
        type: Number,
        default: 0,
    },
});
const group = await DefaultService.getGroupFacultiesFacultyIdGroupsGroupIdGet(
    props.group.faculty.id,
    props.group.id,
    20230904,
    20230910
);
</script>
<style lang="scss" scoped>
.lessons {
    display: flex;
    flex-direction: column;
    gap: 5px;

    @include xl {
        gap: 10px;
    }
}
</style>
