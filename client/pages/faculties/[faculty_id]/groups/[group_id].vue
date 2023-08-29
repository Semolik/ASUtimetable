<template>
    <teleport to="#header-text" v-if="mounted" :disabled="disableTeleport">
        <div class="group-info-container">
            <div class="group-info">
                <nuxt-link
                    class="group-info_block"
                    :to="`/faculties/${groupData.faculty.id}`"
                >
                    {{ groupData.faculty.name }}
                </nuxt-link>
                <div class="group-info_block">
                    {{ groupData.name }}
                </div>
                <div
                    :class="['favorite', { active: isFavorite }]"
                    @click="groupsStore.toggleFavorite(groupData)"
                >
                    <Icon name="material-symbols:favorite" />
                </div>
            </div>
            <div class="group-info">
                <div class="group-info_block button" @click="toWeek(false)">
                    прошлая неделя
                </div>
                <div class="group-info_block">
                    <DatePicker
                        @update:modelValue="getGroupData"
                        @popoverDidShow="popoverShowed = true"
                        @popoverWillHide="popoverShowed = false"
                        mode="range"
                        v-model="range"
                        class="calendar"
                        :is-dark="false"
                        :attributes="attrs"
                        is-range
                        is-expanded
                    >
                    </DatePicker>
                </div>
                <div class="group-info_block button" @click="toWeek(true)">
                    следующая неделя
                </div>
            </div>
        </div>
    </teleport>
</template>
<script setup>
import { DefaultService } from "@/client";
import moment from "moment";
import { useGroupsStore } from "@/store/groups";
import { DatePicker } from "v-calendar";

const groupsStore = useGroupsStore();
const windowWidth = ref(window.innerWidth);
const mounted = ref(false);
onMounted(() => {
    mounted.value = true;
    window.addEventListener("resize", () => {
        windowWidth.value = window.innerWidth;
    });
});
onUnmounted(() => {
    window.removeEventListener("resize", () => {
        windowWidth.value = window.innerWidth;
    });
});
const disableTeleport = computed(() => windowWidth.value < 1200);
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
const range = reactive({
    start: week_start,
    end: week_end,
});
const attrs = [
    {
        key: "today",
        highlight: "red",
        dates: new Date(),
    },
];

const popoverShowed = ref(false);
const calendar = ref(null);
const toWeek = (next = false) => {
    console.log(range);
    let start = moment(range.start)
        .add(next ? 7 : -7, "days")
        .startOf("isoweek")
        .toDate();
    range.start = start;
    range.end = moment(start).add(6, "days").toDate();
};
const getGroupData = async () => {
    groupData.value =
        await DefaultService.getGroupFacultiesFacultyIdGroupsGroupIdGet(
            faculty_id,
            group_id,
            moment(range.start).format("YYYYMMDD"),
            moment(range.end).format("YYYYMMDD")
        );
};
const isFavorite = computed(() => groupsStore.isFavoriteGroup(groupData.value));
const dateSelected = computed(() => {
    return (
        moment(range.start).format("YYYYMMDD") !=
            moment(week_start).format("YYYYMMDD") ||
        moment(range.end).format("YYYYMMDD") !=
            moment(week_end).format("YYYYMMDD")
    );
});
watch([week_end, week_start], () => {
    getGroupData();
});
headerText.value = "";
onMounted(() => {
    mounted.value = true;
});
</script>
<style lang="scss" scoped>
.group-info-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    .group-info {
        border-radius: 16px;
        padding: 8px;
        display: flex;
        color: $accent-1;
        gap: 8px;
        width: 100%;
        padding: 8px;
        background-color: rgba($color: #000000, $alpha: 0.1);
        .group-info_block {
            background-color: rgba($color: #000000, $alpha: 0.1);
            padding: 8px;
        }

        @include md(true) {
            flex-direction: column;
        }

        @include has-hover {
            .button.group-info_block:hover,
            a.group-info_block:hover {
                background-color: rgba($color: #000000, $alpha: 0.2);
                color: #000000;
                cursor: pointer;
            }
        }
        &_block {
            @include flex-center;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 500;
            text-decoration: none;
            flex-grow: 1;
            border-radius: 8px;
        }
    }
    .favorite {
        @include flex-center;
        padding: 16px;
        border-radius: 8px;
        cursor: pointer;
        background-color: rgba($color: #000000, $alpha: 0.1);
        @include has-hover {
            &:hover {
                background-color: rgba($color: #000000, $alpha: 0.2);
            }
        }
        transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
        &.active {
            color: red;
        }

        svg {
            width: 20px;
            height: 20px;
        }
    }
}
</style>
