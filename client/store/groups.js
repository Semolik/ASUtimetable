import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useGroupsStore = defineStore("groups", {
    state: () => ({
        groups: useLocalStorage("groups", []),
        defaultGroup: useLocalStorage("default-group", {}),
    }),
    actions: {
        addGroup(group) {
            this.groups.push(group);
            if (this.groups.length === 1) {
                this.defaultGroup = {
                    faculty_id: group.faculty_id,
                    group_id: group.group_id,
                };
                console.log({
                    faculty_id: group.faculty_id,
                    group_id: group.group_id,
                });
            }
        },
        groupsAreEqual(group1, group2) {
            return (
                group1?.faculty_id === group2?.faculty_id &&
                group1?.group_id === group2?.group_id
            );
        },
        deleteGroup(group) {
            this.groups = this.groups.filter(
                (group_) => !this.groupsAreEqual(group_, group)
            );
            if (this.groupsAreEqual(group, this.defaultGroup)) {
                this.defaultGroup =
                    this.groups.length > 0
                        ? {
                              faculty_id: this.groups[0].faculty_id,
                              group_id: this.groups[0].group_id,
                          }
                        : null;
            }
        },
        setDefault(group) {
            this.defaultGroup = {
                faculty_id: group.faculty_id,
                group_id: group.group_id,
            };
        },
    },
    getters: {
        defaultGroupInfo() {
            return this.groups.find((group) =>
                this.groupsAreEqual(group, this.defaultGroup)
            );
        },
    },
});
