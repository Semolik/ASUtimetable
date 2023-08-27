import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useGroupsStore = defineStore("groups_", {
    state: () => ({
        groups_: useLocalStorage("groups_", []),
        defaultGroup: useLocalStorage("default-group", null),
    }),
    actions: {
        addGroup(group) {
            this.groups_.push(group);
            if (this.groups_.length === 1) {
                this.defaultGroup = {
                    faculty_id: group.faculty_id,
                    group_id: group.group_id,
                };
            }
        },
        groupsAreEqual(group1, group2) {
            return (
                group1?.faculty_id === group2?.faculty_id &&
                group1?.group_id === group2?.group_id
            );
        },
        deleteGroup(group) {
            this.groups_ = this.groups_.filter(
                (group_) => !this.groupsAreEqual(group_, group)
            );
            if (this.groupsAreEqual(group, this.defaultGroup)) {
                this.defaultGroup =
                    this.groups_.length > 0
                        ? {
                              faculty_id: this.groups_[0].faculty_id,
                              group_id: this.groups_[0].group_id,
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
            return this.groups_.find((group) =>
                this.groupsAreEqual(group, this.defaultGroup)
            );
        },
        groups() {
            return this.groups_;
        },
    },
});
