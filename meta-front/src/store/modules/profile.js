import ProfileService from "@/services/ProfileService.js";

export const namespaced = true;

export const state = {
  profiles: [],
  profile: {}
};

export const mutations = {
  SET_ALL_PROFILES(state, profiles) {
    state.profiles = profiles;
  },
  SET_PROFILE(state, profile) {
    state.profile = profile;
  }
};

export const actions = {
  // fetch all profiles from db
  fetchAllProfiles({ commit }) {
    ProfileService.getAllProfiles()
      .then(response => {
        commit("SET_ALL_PROFILES", response.data);
      })
      .catch(error => {
        console.log("There was an error:" + error.message);
      });
  },

  // fetch one profile from db
  fetchProfile({ commit, getters }, id) {
    let profile = getters.getProfileById(id);

    if (profile) {
      commit("SET_PROFILE", profile);
    } else {
      ProfileService.getProfile(id)
        .then(response => {
          console.log(response.data);
          commit("SET_PROFILE", response.data);
        })
        .catch(error => {
          console.log("There was an error:" + error.message);
        });
    }
  }
};

export const getters = {
  getProfileById: state => id => {
    return state.profiles.find(profile => profile.id === id);
  }
};
