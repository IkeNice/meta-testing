<template>
  <div class="profile__list">
    <h1>Profiles List</h1>
    <ProfileCard
      v-for="profile in profile.profiles"
      :key="profile.id"
      :profile="profile"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";

import ProfileCard from "../components/ProfileCard.vue";

export default {
  components: {
    ProfileCard
  },
  created() {
    this.$store.dispatch("profile/fetchAllProfiles");
  },
  computed: {
    ...mapState(["profile"])
  }
};
</script>

<style lang="scss" scoped>
.profile__list {
  display: flex;
  flex-direction: column;
  text-decoration: none;
}
</style>
