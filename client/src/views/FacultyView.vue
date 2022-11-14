<template>
  <HeadlineTemplate :text="'Найти группу'" :data="data" showFacultyData :linkbase="linkbase" />
</template>

<script>
import LinksList from '../components/LinksList.vue';
import { HTTP } from '../http-common.vue';
import HeadlineTemplate from '../components/HeadlineTemplate.vue';

export default {
  components: {
    LinksList,
    HeadlineTemplate,
  },
  data() {
    return {
      data: {},
      faculty_id: this.$router.currentRoute.value.params.faculty_id,
      linkbase: '',
    }
  },


  mounted() {
    if (isNaN(this.faculty_id)) {
      this.$router.push('/404');
    }
    this.linkbase = `/students/${this.faculty_id}/`;
    this.$emit('loading', true);
    HTTP.get('faculty', { params: { faculty_id: this.faculty_id } })
      .then((response) => {
        this.data = response.data;
      })
      .catch((error) => {
        this.$emit('request_error', error);
      }).finally(() => {
        this.$emit('loading', false);
      });
  }
}
</script>

