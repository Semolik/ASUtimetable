<template>
    <ClientOnly>
        <Teleport to="body" v-if="active || isClosing">
            <Transition name="modal">
                <div
                    :class="[
                        'modal-bg',
                        { open: isActive },
                        { close: isClosing },
                        { 'no-justify-content': props.offJustifyContent },
                    ]"
                    v-if="isActive"
                    @click.self="
                        props.closeButton || props.offOutsideClickClose
                            ? null
                            : closeModal()
                    "
                    v-bind="$attrs"
                    @goToLogin="onGoToLogin"
                >
                    <slot name="header"></slot>
                    <div class="modal">
                        <div class="modal-content">
                            <div class="modal-headline" v-if="props.headText">
                                {{ props.headText }}
                            </div>
                            <slot name="content"></slot>
                        </div>
                        <slot name="bottom"></slot>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </ClientOnly>
</template>
<script setup>
const props = defineProps({
    active: Boolean,
    style: Object,
    offJustifyContent: Boolean,
    transition: {
        type: Number,
        default: 250,
    },
    maxWidth: {
        type: [Number, String],
        default: 500,
    },
    maxHeight: {
        type: [Number, null, String],
        default: 800,
    },
    minHeight: {
        type: [Number, null, String],
        default: null,
    },
    offOutsideClickClose: {
        type: Boolean,
        default: false,
    },
    gap: {
        type: Number,
        default: 8,
    },
    headText: {
        type: String,
        default: "",
    },
    closeOnEsckey: {
        type: Boolean,
        default: true,
    },
    borderRadius: {
        type: Number,
        default: 16,
    },
});

const emit = defineEmits(["update:active", "mounted", "close"]);
const transitionString = computed(() => {
    return `${props.transition}ms`;
});
const width = computed(() => {
    if (typeof props.maxWidth === "string") {
        return props.maxWidth;
    }
    return `${props.maxWidth}px`;
});
const height = computed(() => {
    if (props.maxHeight === null) {
        return "auto";
    }
    if (typeof props.maxHeight === "string") {
        return props.maxHeight;
    }
    return `${props.maxHeight}px`;
});
const borderRadius = computed(() => {
    return `${props.borderRadius}px`;
});
const gapString = computed(() => {
    return `${props.gap}px`;
});
const minHeight = computed(() => {
    if (props.minHeight === null) {
        return "auto";
    }
    if (typeof props.minHeight === "string") {
        return props.minHeight;
    }
    return `${props.minHeight}px`;
});
const isClosing = ref(false);
const isActive = ref(true);
const closeModal = () => {
    isClosing.value = true;
    setTimeout(() => {
        emit("update:active", false);
        emit("close");
        isActive.value = false;
        isClosing.value = false;
    }, props.transition);
};
if (props.closeOnEsckey) {
    onMounted(() => {
        window.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && props.active) {
                closeModal();
            }
        });
    });
}
const openModal = () => {
    isActive.value = true;
    setTimeout(() => {
        emit("mounted");
    }, props.transition);
};
watch(
    () => props.active,
    (value) => {
        if (value) {
            openModal();
        } else {
            closeModal();
        }
    }
);
</script>
<style lang="scss">
.modal-enter-active,
.modal-leave-active {
    transition: all v-bind(transitionString) ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-bg {
    position: fixed;
    inset: 0;
    background-color: rgba($color: #000000, $alpha: 0.3);
    @include flex-center;
    z-index: 2000;
    opacity: 0;

    flex-direction: column;
    transition: opacity v-bind(transitionString) ease-in-out;
    backdrop-filter: blur(8px);
    padding: 10px;
    &.open {
        animation: open v-bind(transitionString) ease-in-out;
        opacity: 1;
    }
    &.close {
        animation: close v-bind(transitionString) ease-in-out;
        opacity: 0;
    }
    &.no-justify-content {
        justify-content: unset;
    }
    @keyframes open {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
    @keyframes close {
        0% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }

    .modal {
        background-color: $secondary-color;
        max-width: v-bind(width);
        max-height: v-bind(height);
        width: 100%;
        border-radius: v-bind(borderRadius);
        display: flex;
        flex-direction: column;
        padding: 10px;
        gap: v-bind(gapString);
        overflow: auto;
        min-height: v-bind(minHeight);

        .modal-content {
            height: 100%;
            display: flex;
            flex-direction: column;
            gap: v-bind(gapString);
            .modal-headline {
                font-size: 1.1rem;
                text-align: center;
            }
        }
    }
}
</style>
