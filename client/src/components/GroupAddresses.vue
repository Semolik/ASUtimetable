<template>
    <div class="addresses" v-if="addresses">
        <div class="address" v-for="address in addresses">
            <div class="line">
                <div class="block letter">{{address.letter}}</div>
                <div class="block faculties">{{address.faculties}}</div>
            </div>
            <div class="block address-info">{{address.address}}</div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        data: Object,
    },
    computed: {
        addresses() {
            return this.data?.addresses || []
        },
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';

.addresses {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;

    .address {
        display: flex;
        flex-wrap: wrap;
        border-radius: 15px;
        overflow: hidden;
        flex-grow: 1;

        .line {
            display: flex;
            flex-wrap: wrap;
            flex-grow: 1;

            .block {
                &.letter {
                    background-color: var(--red-0);
                }
            }
        }

        .block {
            flex-grow: 1;
            text-align: center;
            @include helpers.flex-center;
            padding: 10px 15px;

            &.address-info {
                @include themes.dark {
                    background-color: var(--color-background-mute-3);
                }

                @include themes.light {
                    box-shadow: var(--main-card-shadow);
                }
            }
        }

        @include themes.dark {
            background-color: var(--color-background-mute-2);
        }

        @include themes.light {
            background-color: var(--main-card-border);

        }
    }
}
</style>