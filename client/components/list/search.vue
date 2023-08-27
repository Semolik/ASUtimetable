<template>
    <div class="search-list">
        <div :class="['search', { active: active }]">
            <input
                type="text"
                v-model="search"
                @focus="active = true"
                @blur="active = false"
                :placeholder="placeholder"
            />
            <AnimateInteger class="count" :value="searchedItems.length" />
        </div>
        <list>
            <slot :items="searchedItems" />
        </list>
        <div class="empty" v-if="!searchedItems.length">
            <div class="message">Ничего не найдено</div>
        </div>
    </div>
</template>
<script setup>
const { items, searchPropety, placeholder } = defineProps({
    items: {
        type: Array,
        required: true,
    },
    searchPropety: {
        type: String,
        default: "name",
    },
    placeholder: {
        type: String,
        default: "Найти",
    },
});
const search = ref("");
const active = ref(false);
const searchedItems = computed(() => {
    return items.filter((item) => {
        return item[searchPropety]
            .toLowerCase()
            .includes(search.value.toLowerCase());
    });
});
</script>

<style lang="scss" scoped>
.search-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    position: relative;

    .search {
        position: relative;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0px 10px;
        border-radius: 10px;
        background-color: rgba($color: #000000, $alpha: 0.1);
        transition: 0.3s;
        cursor: pointer;

        &.active {
            background-color: rgba($color: #000000, $alpha: 0.15);

            .count {
                color: $accent-1;
            }
        }

        input {
            background-color: transparent;
            border: none;
            padding: 10px 8px;
            font-size: 1.1em;
            outline: none;
            width: 100%;
        }

        .count {
            position: absolute;
            right: 10px;
            font-size: 14px;
            color: $text-color-2;
        }
    }

    .empty {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        .message {
            color: $text-color-2;
        }
    }
}
</style>
