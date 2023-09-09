<template>
    <div class="groups">
        <div class="groups-buttons">
            <nuxt-link :to="{ name: 'faculties' }" class="button">
                <div class="text">Добавить группу</div>
            </nuxt-link>
        </div>
        <template v-if="!groups.length">
            <div class="empty-groups">
                <div class="text">Здесь пока пусто</div>
            </div>
        </template>
        <div class="groups-container">
            <group-block
                v-for="group in groups"
                :key="group.id"
                :group="group"
            />
        </div>
    </div>
</template>
<script setup>
import { useGroupsStore } from "@/store/groups";
import { storeToRefs } from "pinia";

const groupsStore = useGroupsStore();
const { groups } = storeToRefs(groupsStore);
headerText.value = "Расписание";
</script>
<style lang="scss" scoped>
.groups {
    display: grid;
    grid-template-rows: min-content 1fr;
    gap: 10px;

    .groups-buttons {
        display: flex;
        justify-content: right;
        gap: 10px;

        .button {
            padding: 5px 15px;
            line-height: 20px;
            text-decoration: none;
            border-radius: 20px;
            cursor: pointer;
            background-color: $tetriary-background;

            @include has-hover {
                background-color: $qiunary-background;
            }
        }
    }

    .empty-groups {
        padding: 1.5rem;
        border: 2px dashed $primary-text;
        border-radius: 10px;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

        .text {
            font-size: large;
        }
    }

    .groups-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
    }
}
</style>
