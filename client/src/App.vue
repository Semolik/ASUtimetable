<script >
import { RouterView } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import { hasTouch } from 'detect-touch';
import { computed } from 'vue';
import AppError from './components/AppError.vue';
import handleError from './composables/errors';

export default {
  components: {
    RouterView,
    AppHeader,
    AppError
  },
  data() {
    return {
      enableHover: !hasTouch,
      loading: false,
      windowWidth: window.innerWidth,
      blur_content: false,
      error: null,
      nowTime: Date.now(),
    }
  },
  provide() {
    return {
      enableHover: !hasTouch,
      loading: computed(() => this.loading),
      windowWidth: computed(() => this.windowWidth),
      nowTime: computed(() => this.nowTime),
      disableLoading: false,
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    });
    setInterval(() => {
      this.nowTime = Date.now();
    }, 1000)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  methods: {
    setLoading(status) {
      this.loading = status;
    },
    blurAppContent(value) {
      console.log(value)
      this.blur_content = value;

    },
    onResize() {
      this.windowWidth = window.innerWidth
    },
    hideBodyOverflow(value) {
      console.log(value)
      document.body.style.overflow = value ? 'hidden' : '';
    },

    setError(data) {
      this.error = data;
    },
    handleAppError(error) {
      this.error = handleError(error);
    }
  },

}

</script>

<template >
  <AppHeader @blur_content="blurAppContent" @hide_body_overflow="hideBodyOverflow" />
  <div :class="['app-content', { hoverable: enableHover }, { blur: blur_content }]">
    <router-view v-slot="{ Component, route }">
      <transition name="list" mode="out-in">
        <div :key="route.name" class="transition-wrapper">
          <component :is="Component" @loading="setLoading" @request_error="handleAppError" @error="setError"
            v-if="!error" />
          <AppError @reset_error="error = null" v-else :inputMessage="error.message" :inputStatusCode="error.status" />
        </div>
      </transition>
    </router-view>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/animations';

.app-content {
  margin-right: calc(-1 * (100vw - 100%));
  --padding-app: calc(var(--header-height) + 1rem);
  padding-inline: 20px;
  padding-top: var(--padding-app);
  padding-bottom: 10px;
  transition: filter .3s;

  @media only screen and (hover: none) {
    padding-inline: 10px;
  }

  &.blur {
    filter: blur(10px);
  }

  .transition-wrapper {
    min-height: calc(100vh - var(--padding-app) - 1rem);
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  @include animations.list;
}
</style>
