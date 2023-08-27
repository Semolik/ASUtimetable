<template>
    <ListSearch :items="faculties" searchPropety="name">
        <template #default="{ items }">
            <ListItem
                :to="`/faculties/${item.id}`"
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
headerText.value = "Факультеты";
const faculties = await DefaultService.getFacultiesFacultiesGet();
</script>
