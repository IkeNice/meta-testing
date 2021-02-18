<template>
  <div>
    <div class="profile__container">
      <div class="profile__image">
        <img :src="profile.photo" alt="Фотография" />
      </div>
      <div class="profile__body">
        <div class="profile__name">
          ФИО: <span class="name__span">{{ profile.name }}</span>
        </div>
        <h4 class="methods__header">Методы:</h4>
        <div class="profile__methods">
          <div
            class="method"
            v-for="method in profile.methods.split(',')"
            :key="method"
          >
            {{ method | methodFilter }}
          </div>
        </div>
      </div>
    </div>
    <router-link to="/">
      <div class="go__back">К списку</div>
    </router-link>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  props: ["id"],
  created() {
    this.$store.dispatch("profile/fetchProfile", this.id);
  },
  computed: {
    ...mapState({
      profile: state => state.profile.profile
    })
  },
  filters: {
    methodFilter: value => {
      return value.replace(/[[\]"']/g, "");
    }
  }
};
</script>

<style lang="scss">
.profile__container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;

  display: flex;
}

/* Profile Image */
.profile__image {
  height: 100%;
  width: 400px;
  margin: 20px;
}
img {
  max-width: 100%;
  max-height: 100%;
}

/* Profile Body */
.profile__body {
  margin-top: 20px;
  flex-grow: 1;
}
/* Name */
.profile__name {
  text-align: start;
  font-weight: 700;
}
.name__span {
  margin: 0 auto;
}

/* Methods */
.methods__header {
  text-align: start;
}
.profile__methods {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 15px;
}
.method {
  background: lightgrey;
  padding: 5px 15px;
}

/* Go Back */
.go__back {
  margin: 0 auto;
  padding: 3px;
  width: 5%;

  background: lightgrey;
  color: black;
}
</style>
