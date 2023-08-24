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
                <div class="field">
                    <label>Группа по умолчанию</label>
                    <USelectMenu
                        :model-value="defaultGroup"
                        @update:model-value="groupsStore.setDefault"
                        :options="groups"
                        :disabled="!defaultGroup"
                        option-attribute="name"
                        size="xl"
                        placeholder="dasdas"
                    >
                        <template #label v-if="defaultGroup">
                            {{ defaultGroupInfo.name }}
                        </template>
                        <template #label v-else> Нет избранных групп </template>
                    </USelectMenu>
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
.field {
    display: flex;
    flex-direction: column;
    gap: 2px;
    label {
        font-size: 14px;
    }
}
</style>
