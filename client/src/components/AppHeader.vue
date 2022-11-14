<template>
    <header :class="{ active: nav_opened }">
        <router-link to="/" class="text" @click="this.$emit('reset_error')">Расписание</router-link>
        <div class="buttons">
            <div :class="['themeswitch', 'button', themeName]" @click="toggleTheme">
                <div class="icons">
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-sun" />
                    </div>
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-moon" />
                    </div>
                </div>
            </div>
            <div :class="['nav-toggle', 'button', { active: nav_opened }]" @click="toggleNav">
                <div class="icon on">
                    <FontAwesomeIcon icon="fa-xmark" />
                </div>
                <div class="icon off">
                    <FontAwesomeIcon icon="fa-bars" />
                </div>
            </div>
        </div>

    </header>
    <div :class="['nav-container', { active: nav_opened }]" @click.self="toggleNav">
        <nav :class="{ hoverable: enableHover }">
            <a :href="link.url" class="link" target="_blank" rel="noopener noreferrer" v-for="link in links">
                <div class="link-text">{{ link.name }}</div>
            </a>
        </nav>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSun, faMoon, faBars, faXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useThemeStore } from '../stores/theme';
import { storeToRefs } from 'pinia';

library.add([faSun, faMoon, faBars, faXmark]);

export default {
    setup() {
        const themeStore = useThemeStore();
        const { themeName } = storeToRefs(themeStore);
        const { toggleTheme } = themeStore;
        return {
            themeName,
            toggleTheme,
        }
    },
    components: {
        FontAwesomeIcon,
    },
    inject: ['enableHover'],
    emits: ['blur_content', 'hide_body_overflow'],
    methods: {
        toggleNav() {
            this.nav_opened = !this.nav_opened;
            this.$emit('blur_content', this.nav_opened);
        }
    },
    data() {
        return {
            themeToggle: false,
            nav_opened: false,
            links: [
                {
                    'name': 'Образовательный портал',
                    'url': 'https://portal.edu.asu.ru/my'
                },
                {
                    'name': 'Сайт университета',
                    'url': 'https://asu.ru'
                },
                {
                    'name': 'Главная страница',
                    'url': 'https://semolik.ru'
                },
            ],
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';

$header-background: rgba(var(--color-background-rgb), 0.5);

header {
    position: fixed;
    display: flex;
    align-items: center;
    width: 100%;
    height: var(--header-height);
    padding: 1rem;
    gap: 10px;
    z-index: 10;
    backdrop-filter: blur(10px);
    background-color: $header-background;
    border-bottom: 1px solid var(--color-background-mute);
    transition: border-color .2s;

    &.active {
        border-bottom-color: transparent;
        background-color: var(--color-background);
    }

    .text {
        font-size: x-large;
        margin-right: auto;
        height: min-content;
        color: var(--color-header-text);
        text-decoration: none;
    }

    .buttons {
        display: flex;
        gap: 10px;


        .button {
            height: 40px;
            width: 40px;
            border-radius: 50%;

            .icon {
                width: 100%;
                height: 100%;
                padding: 8px;

                svg {
                    color: black;
                    width: 100%;
                    height: 100%;
                }
            }
        }

        .nav-toggle {
            background-color: var(--nav-toggle-color);
            position: relative;

            &.active {
                .icon {
                    &.on {
                        opacity: 1;
                        transform: rotate(0deg);
                    }

                    &.off {
                        opacity: 0;
                        transform: rotate(90deg);
                    }
                }
            }

            .icon {
                &.on {
                    opacity: 0;
                    transform: rotate(90deg);
                }

                &.off {
                    opacity: 1;
                    transform: rotate(0deg);
                }

                transition: opacity .2s,
                transform .2s;
                position: absolute;
            }
        }

        .themeswitch {
            position: relative;
            overflow: hidden;

            &.light {
                background-color: var(--light-theme-toggle-color);
            }

            &.dark {
                background-color: var(--dark-theme-toggle-color);

                .icons {
                    top: -100%;
                }
            }

            .icons {
                position: absolute;
                top: 0;
                width: 100%;
                height: 100%;
                transition: .2s top;
            }
        }
    }
}

.nav-container {
    position: fixed;
    z-index: 9;
    top: var(--header-height);
    transition: left .3s;
    left: -100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    height: 100%;

    &.active {
        left: 0;
    }

    nav {
        padding: 10px;
        display: flex;
        gap: 10px;
        background-color: var(--color-background);

        @include breakpoints.lg(true) {
            flex-direction: column;
        }


        &.hoverable {
            .link {
                &:hover {
                    @include themes.light {
                        background-color: var(--color-text);
                        color: var(--color-text-rev);
                    }

                    @include themes.dark {
                        background-color: var(--color-background-mute-3);
                    }
                }
            }
        }

        .link {
            width: 100%;
            min-width: 300px;
            text-decoration: none;
            @include helpers.flex-center;
            text-align: center;
            color: var(--color-text);
            font-size: 1.1em;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid transparent;

            @include themes.light {
                background-color: transparent;
                border-color: var(--color-text);
            }

            @include themes.dark {
                background-color: var(--color-background-mute-2);
            }
        }
    }
}
</style>