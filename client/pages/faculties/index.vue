<template>
    <div class="faculties">
        <nuxt-link
            class="faculty"
            v-for="faculty in faculties"
            :key="faculty.id"
            :to="`/faculties/${faculty.id}`"
        >
            {{ faculty.name }}
        </nuxt-link>
    </div>
</template>
<script setup>
import { DefaultService } from "@/client";
const faculties = await DefaultService.getFacultiesFacultiesGet();
</script>
<style scoped lang="scss">
.faculties {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;

    .faculty {
        @include flex-center;
        padding: 20px 10px;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        background-color: rgba($color: #000000, $alpha: 0.1);

        &:hover {
            background-color: rgba($color: #000000, $alpha: 0.2);
        }
    }
}
</style>
