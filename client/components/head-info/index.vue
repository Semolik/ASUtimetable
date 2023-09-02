<template>
    <head-info-container>
        <div :class="['search', { active: active }]">
            <input
                type="text"
                v-model="input"
                @focus="active = true"
                @blur="active = false"
                :placeholder="text"
                ref="search"
            />
            <AnimateInteger class="count" :value="searchedItems.length" />
        </div>
        <list>
            <slot :items="searchedItems" />
        </list>
    </head-info-container>
</template>

<script setup>
const { allItems, text } = defineProps({
    allItems: Array,
    text: String,
});
const active = ref(false);
const input = ref("");
const searchedItems = computed(() => {
    let text = input.value.toLowerCase();
    if (!text) return allItems;
    return allItems.filter((item) => {
        return item.name.toLowerCase().includes(text);
    });
});
</script>

<style scoped lang="scss">
.search {
    margin: auto;
    display: flex;
    width: 100%;
    height: 50px;
    position: relative;
    background-color: $secondary-background;
    border-radius: 10px;
    overflow: hidden;

    .count {
        aspect-ratio: 1;
        height: 100%;
        @include flex-center;
        color: $quternary-text;
        transition: all 0.2s ease-in-out;
    }

    input {
        background-color: $secondary-background;
        border: none;
        padding: 8px 10px;
        color: $quternary-text;
        font-size: 1.1em;
        outline: none;
        width: 100%;
    }

    &.active {
        background-color: $secondary-background;

        .count {
            color: $primary-text;
        }

        input {
            outline: none;
            background-color: $secondary-background;
            color: $primary-text;
        }
    }
}
</style>
