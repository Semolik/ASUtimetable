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
                    :class="[
                        'group-info_block favorite button',
                        { active: isFavorite },
                    ]"
                    @click="groupsStore.toggleFavorite(groupData)"
                >
                    <Icon name="material-symbols:favorite" />
                </div>
            </div>
            <div class="group-info">
                <div class="group-info_block button" @click="toWeek(false)">
                    <span>прошлая неделя</span>
                    <Icon name="material-symbols:arrow-back-rounded" />
                </div>

                <DatePicker
                    @update:modelValue="getGroupData"
                    mode="range"
                    v-model.range="range"
                    class="calendar"
                    is-dark
                    :attributes="attrs"
                    :popover="false"
                    ref="calendar"
                    is-range
                    is-expanded
                >
                    <template v-slot="{ inputValue, togglePopover }">
                        <div
                            class="group-info_block button date"
                            @click="
                                togglePopover({
                                    placement: 'bottom',
                                })
                            "
                        >
                            <template v-if="dateSelected">
                                {{ inputValue.start }} -
                                {{ inputValue.end }}
                            </template>
                            <div v-else>выбрать даты</div>
                        </div>
                    </template>
                </DatePicker>
                <div class="group-info_block button" @click="toWeek(true)">
                    <span>следующая неделя</span>
                    <Icon name="material-symbols:arrow-forward-rounded" />
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
const calendar = ref(null);
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
const toWeek = (next) => {
    let start = moment(range.start)
        .add(next ? 7 : -7, "days")
        .startOf("isoweek")
        .toDate();
    var end = moment(start).add(6, "days").toDate();

    calendar.value.updateValue({
        start: start,
        end: end,
    });
    range.start = start;
    range.end = end;
};
const getGroupData = async (A) => {
    console.log(A);
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
watch([() => week_end, () => week_start], () => {
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
    width: 100%;
    gap: 10px;
    color: $primary-text;
    border-radius: 20px;
    margin: 0 auto;
    max-width: 1400px;
    @include lg {
        background-color: $secondary-background;
    }

    @include xl {
        padding: 10px;
    }

    .group-info {
        display: flex;
        gap: 10px;
        @include lg(true) {
            flex-wrap: wrap;
            background-color: $secondary-background;
            border-radius: 20px;
            padding: 10px;
        }
        .calendar {
            width: 100%;
        }
        .group-info_block.button,
        a.group-info_block {
            cursor: pointer;
            @include has-hover {
                background-color: $qiunary-background;
            }
        }

        .group-info_block {
            background-color: $quaternary-background;
            border-radius: 10px;
            padding: 10px 30px;
            display: flex;
            flex-grow: 1;
            user-select: none;
            @include flex-center;

            &.date {
                padding: 10px;
            }
            text-align: center;
            svg {
                width: 24px;
                height: 24px;
                fill: $primary-text;
                @include md {
                    display: none;
                }
            }

            @include md(true) {
                span {
                    display: none;
                }
            }

            &.favorite {
                cursor: pointer;
                min-width: 50px;
                @include lg {
                    flex-grow: 0;
                }
                svg {
                    display: block;
                    transition: 0.3s;
                }

                &.active {
                    svg {
                        color: $accent-red-2;
                    }
                }
            }
        }
    }
}
</style>
