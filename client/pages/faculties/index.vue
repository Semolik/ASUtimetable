<template>
    <HeadInfo text="Найти факультет" :all-items="faculties">
        <template #default="{ items }">
            <ListItem
                :to="{
                    name: 'faculties-faculty_id',
                    params: { faculty_id: faculty.id },
                }"
                v-for="faculty in items"
                :key="faculty.id"
            >
                {{ faculty.name }}
            </ListItem>
        </template>
    </HeadInfo>
</template>
<script setup>
import { DefaultService } from "@/client";

const faculties = await DefaultService.getFacultiesFacultiesGet();
</script>
