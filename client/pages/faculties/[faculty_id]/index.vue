<template>
    <HeadInfo text="Найти факультет" :all-items="faculty.groups">
        <template #default="{ items }">
            <ListItem
                :to="{
                    name: 'faculties-faculty_id-groups-group_id',
                    params: { faculty_id, group_id: item.id },
                }"
                v-for="item in items"
                :key="item.id"
            >
                {{ item.name }}
            </ListItem>
        </template>
    </HeadInfo>
</template>
<script setup>
import { DefaultService } from "@/client";
const { faculty_id } = useRoute().params;
const faculty = await DefaultService.getFacultyFacultiesFacultyIdGet(
    faculty_id
);
</script>
