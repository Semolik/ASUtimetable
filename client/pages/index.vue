<template>
    <div class="index-page">
        <div class="groups">
            <div
                v-for="group in groups"
                :class="[
                    'group',
                    { active: groupsStore.groupsAreEqual(group, currentGroup) },
                ]"
                @click="currentGroup = group"
            >
                {{ group.name }}
            </div>
        </div>
        <div
            @click="
                () => {
                    groups.length = 0;
                    defaultGroup = null;
                }
            "
        >
            clear
        </div>
        <div
            class="plus-button"
            @click="
                () => {
                    groupsStore.addGroup({
                        faculty_id: increment,
                        group_id: increment,
                        name: `group ${increment}`,
                    });
                    increment++;
                }
            "
        >
            <Icon name="material-symbols:add-rounded" />
        </div>
    </div>
</template>
<script setup>
import { useGroupsStore } from "@/store/groups";
import { storeToRefs } from "pinia";
const groupsStore = useGroupsStore();
const { groups, defaultGroup } = storeToRefs(groupsStore);
const currentGroup = ref(defaultGroup.value);

watch(defaultGroup, (newdefaultGroup) => {
    currentGroup.value = newdefaultGroup;
});
const increment = ref(1);
</script>
<style lang="scss" scoped>
.index-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
    height: 100%;
    padding: 0px 10px;

    .plus-button {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: $accent-1;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        svg {
            width: 25px;
            height: 25px;
            color: $secondary-color;
        }
    }
    .groups {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        .group {
            padding: 5px 16px;
            border-radius: 16px;
            color: $text-color-2;
            cursor: pointer;
            font-weight: 500;
            background-color: transparent;
            white-space: nowrap;
            transition: background-color 0.2s ease, color 0.2s ease;
            &.active {
                background-color: $accent-1;
                color: $secondary-color;
            }
        }
    }
}
</style>
