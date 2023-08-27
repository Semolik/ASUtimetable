<template>
    <header>
        <nuxt-link to="/" class="settings-button">
            <Icon name="material-symbols:home" />
        </nuxt-link>
        <div class="header-text" id="header-text">{{ headerText }}</div>
        <div
            class="settings-button"
            @click="settingsModalActive = !settingsModalActive"
        >
            <Icon name="material-symbols:settings" />
        </div>

        <Modal v-model:active="settingsModalActive" :min-height="500">
            <template #content>
                <div class="field">
                    <label>Группа по умолчанию</label>
                    <USelectMenu
                        :model-value="defaultGroup"
                        @update:model-value="groupsStore.setDefault"
                        :options="groups"
                        :disabled="!defaultGroup"
                        option-attribute="name"
                        size="xl"
                    >
                        <template #label>
                            <span v-if="defaultGroup">{{
                                defaultGroupInfo?.name
                            }}</span>
                            <span v-else>Нет избранных групп</span>
                        </template>
                    </USelectMenu>
                </div>
                <div
                    class="border border-gray-200 not-prose rounded-md bg-white h-full overflow-scroll"
                >
                    <UTable :rows="groups" :columns="columns">
                        <template #actions-data="{ row }">
                            <div class="flex justify-end">
                                <UButton
                                    color="gray"
                                    variant="ghost"
                                    icon="i-heroicons-trash"
                                    @click="groupsStore.deleteGroup(row)"
                                />
                            </div>
                        </template>
                        <template #empty-state>
                            <div
                                class="flex flex-col items-center justify-center py-6 gap-3 h-full"
                            >
                                <nuxt-link
                                    to="/faculties"
                                    @click="settingsModalActive = false"
                                >
                                    <UButton label="Добавить группу" />
                                </nuxt-link>
                            </div>
                        </template>
                    </UTable>
                </div>
            </template>
        </Modal>
    </header>
</template>
<script setup>
import { useGroupsStore } from "@/store/groups";
import { storeToRefs } from "pinia";
const groupsStore = useGroupsStore();
const { groups, defaultGroup, defaultGroupInfo } = storeToRefs(groupsStore);
const columns = [
    {
        key: "name",
        label: "Группа",
    },
    {
        key: "faculty_id",
        label: "Факультет",
    },

    {
        key: "actions",
    },
];
const settingsModalActive = ref(false);
</script>
<style lang="scss" scoped>
header {
    color: $accent-1;
    padding: 10px;
    padding-bottom: 0px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    .header-text {
        font-size: 1.2rem;
        color: $accent-1;
        text-decoration: none;
        font-weight: 500;
        width: 100%;
        @include flex-center;
        height: 100%;
    }
    .settings-button {
        background-color: $secondary-color;
        padding: 16px;
        cursor: pointer;
        box-shadow: $shadow-1;
        border-radius: 16px;
        svg {
            width: 25px;
            height: 25px;
        }
    }
}
.field {
    display: flex;
    flex-direction: column;
    gap: 2px;
    label {
        font-size: 14px;
    }
}
</style>
