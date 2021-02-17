<template>
  <router-link
    class="profile__link"
    :to="{ name: 'profile-show', params: { id: profile.id } }"
  >
    <div class="profile__card">
      <div class="card__img">
        <img
          :src="
            profile['fields']['Фотография'][0]['thumbnails']['small']['url']
          "
          alt="card photo"
        />
      </div>
      <div class="card__body">
        {{ profile["fields"]["Имя"] }}
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  props: {
    profile: Object
  }
};
</script>

<style lang="scss" scoped>
.profile__card {
  display: flex;

  padding: 20px;
  transition: all 0.2s linear;
  cursor: pointer;

  background: lightblue;
}
.profile__card:hover {
  transform: scale(1.01);
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.2), 0 1px 15px 0 rgba(0, 0, 0, 0.19);
}
.profile__link {
  color: black;
  text-decoration: none;
  font-weight: 700;

  width: 100%;
  max-width: 400px;
  margin: 12px auto;
}

.card__body {
  flex-grow: 1;
}
</style>
