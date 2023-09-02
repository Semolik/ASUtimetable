import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useGroupsStore = defineStore("groups", {
    state: () => ({
        groups: useLocalStorage("groups", []),
    }),
    actions: {
        addGroup(group) {
            if (this.groups.length === 0) {
                this.defaultGroup = group;
            }
            this.groups.push(group);
        },
        groupsAreEqual(group1, group2) {
            return (
                group1?.faculty?.id === group2?.faculty?.id &&
                group1?.id === group2?.id
            );
        },
        deleteGroup(group) {
            this.groups = this.groups.filter(
                (group_) => !this.groupsAreEqual(group_, group)
            );
            if (this.groupsAreEqual(group, this.defaultGroup)) {
                this.defaultGroup =
                    this.groups.length > 0 ? this.groups[0] : null;
            }
        },
        toggleFavorite(group) {
            if (this.isFavoriteGroup(group)) {
                this.deleteGroup(group);
            } else {
                this.addGroup(group);
            }
        },
        isFavoriteGroup(group) {
            return this.groups.some((group_) =>
                this.groupsAreEqual(group_, group)
            );
        },
    },
});
