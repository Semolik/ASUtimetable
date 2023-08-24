<template>
    <header>
        <nuxt-link to="/" class="header-text">Расписание</nuxt-link>
        <div
            class="settings-button"
            @click="settingsModalActive = !settingsModalActive"
        >
            <Icon name="material-symbols:settings" />
        </div>

        <Modal v-model:active="settingsModalActive" :min-height="500">
            <template #content>
                <USelectMenu
                    v-model="selected"
                    :options="groupsWithLabels"
                    :disabled="!defaultGroup"
                >
                    <template #label v-if="defaultGroup">
                        {{ selected?.name }}
                    </template>
                    <template #label v-else> Нет избранных групп </template>
                </USelectMenu>
            </template>
        </Modal>
    </header>
</template>
<script setup>
import { useGroupsStore } from "@/store/groups";
import { storeToRefs } from "pinia";
const groupsStore = useGroupsStore();
const { groups, defaultGroup } = storeToRefs(groupsStore);
const groupsWithLabels = computed(() =>
    groups.value.map((group) => ({ ...group, label: group.name }))
);
const selected = ref(defaultGroup.value);
const settingsModalActive = ref(false);
</script>
<style lang="scss" scoped>
header {
    color: $accent-1;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .header-text {
        font-size: 1.5rem;
        color: $accent-1;
        text-decoration: none;
        font-weight: 500;
    }
    .settings-button {
        background-color: $secondary-color;
        padding: 16px;
        cursor: pointer;
        box-shadow: $shadow-1;
        border-radius: 16px;
        svg {
            width: 20px;
            height: 20px;
        }
    }
}
</style>
