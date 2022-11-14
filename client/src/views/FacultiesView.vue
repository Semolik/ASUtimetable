<template>
  <HeadlineTemplate v-bind:linkbase="'/students/'" v-bind:text="'Найти факультет'" v-bind:data="data" />
</template>

<script>
import LinksList from '../components/LinksList.vue';
import { HTTP } from '../http-common.vue';
import HeadlineTemplate from '../components/HeadlineTemplate.vue';

export default {
  components: {
    LinksList,
    HeadlineTemplate
  },
  data() {
    return {
      data: {},
    }
  },
  mounted() {
    this.$emit('loading', true);
    HTTP.get('faculties')
      .then(response => {
        this.data = response.data;
      })
      .catch(error => {
        this.$emit('request_error', error);
      })
      .finally(() => {
        this.$emit('loading', false);
      });
  }
}
</script>

