<template>
    <ListSearch :items="faculty.groups" searchPropety="name">
        <template #default="{ items }">
            <ListItem
                :to="`/faculties/${faculty.id}/groups/${item.id}`"
                v-for="item in items"
                :key="item.id"
            >
                {{ item.name }}
            </ListItem>
        </template>
    </ListSearch>
</template>
<script setup>
import { DefaultService } from "@/client";
const { faculty_id } = useRoute().params;
const faculty = await DefaultService.getFacultyFacultiesFacultyIdGet(
    faculty_id
);
headerText.value = faculty.name;
</script>
