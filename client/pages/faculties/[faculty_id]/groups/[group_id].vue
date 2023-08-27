<template>
    <Teleport to="#header-text" :disabled="disableTeleport" v-if="mounted">
        <div :class="['group-info', { active: !disableTeleport }]">
            <nuxt-link
                class="group-info_block"
                :to="`/faculties/${groupData.faculty.id}`"
            >
                {{ groupData.faculty.name }}
            </nuxt-link>
            <div class="group-info_block">
                {{ groupData.name }}
            </div>
        </div>
    </Teleport>
</template>
<script setup>
import { DefaultService } from "@/client";
import moment from "moment";
const windowWidth = ref(window.innerWidth);
const mounted = ref(false);
onMounted(() => {
    mounted.value = true;
    window.addEventListener("resize", () => {
        windowWidth.value = window.innerWidth;
    });
});
onUnmounted(() => {
    window.removeEventListener("resize");
});
const disableTeleport = computed(() => windowWidth.value < 768);
const { faculty_id, group_id } = useRoute().params;
var now_moment = moment();
var week_start = now_moment.startOf("isoweek").toDate();
week_start.setHours(0, 0, 0, 0);
var week_end = now_moment.endOf("isoweek").toDate();
week_end.setHours(0, 0, 0, 0);
const groupData = ref(
    await DefaultService.getGroupFacultiesFacultyIdGroupsGroupIdGet(
        faculty_id,
        group_id
    )
);
const getGroupData = async () => {
    groupData.value =
        await DefaultService.getGroupFacultiesFacultyIdGroupsGroupIdGet(
            faculty_id,
            group_id,
            moment(week_start).format("YYYYMMDD"),
            moment(week_end).format("YYYYMMDD")
        );
};

watch([week_end, week_start], () => {
    getGroupData();
});
headerText.value = "";
</script>
<style lang="scss" scoped>
.group-info {
    background-color: rgba($color: #000000, $alpha: 0.1);
    width: 100%;
    border-radius: 16px;
    padding: 8px;
    display: flex;
    border-radius: 8px;
    color: $accent-1;

    &.active {
        height: 100%;
    }
    &:not(.active) {
        padding: 16px 8px;
    }
    @include has-hover {
        a.group-info_block:hover {
            background-color: rgba($color: #000000, $alpha: 0.2);
            color: #000000;
        }
    }
    &_block {
        width: 100%;
        @include flex-center;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 500;
        text-decoration: none;
        height: 100%;
        border-radius: 8px;
    }
}
</style>
