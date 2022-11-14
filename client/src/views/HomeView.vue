<template>
  <div class="groups">
    <div class="groups-buttons">
      <router-link to="/students" :class="['button', { hoverable: enableHover }]">
        <div class="text">Добавить группу</div>
      </router-link>
    </div>
    <template v-if="groupsEmpty">
      <div class="empty-groups">
        <div class="text">
          Здесь пока пусто
        </div>
      </div>
    </template>
    <div class="groups-container">
      <HomeViewGroup :groupData="group" v-for="(group, index, key) in groups" :key="key" />
    </div>
  </div>
</template>

<script>
import { useGroupsStore } from '../stores/groups';
import { storeToRefs } from 'pinia';
import HomeViewGroup from '../components/HomeViewGroup.vue';

export default {
  setup() {
    const groupsStore = useGroupsStore();
    const { groups } = storeToRefs(groupsStore);
    return {
      groups
    };
  },
  computed: {
    groupsEmpty() {
      return this.groups.length === 0;
    },
  },
  components: { HomeViewGroup },
  inject: ['enableHover']
}
</script>

<style lang="scss">
@use '../assets/styles/breakpoints';

.groups {
  width: 100%;
  max-width: 1200px;
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
      color: var(--color-text);
      background-color: var(--color-background-mute-2);
      border-radius: 20px;
      cursor: pointer;

      &.hoverable:hover {
        background-color: var(--color-background-mute-3);
      }
    }
  }

  .empty-groups {
    padding: 1.5rem;
    border: 2px dashed var(--color-text);
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
    display: grid;
    gap: 10px;
  }
}
</style>