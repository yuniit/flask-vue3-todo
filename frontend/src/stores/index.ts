import { defineStore } from 'pinia'

type User = {
  _id: string
  username: string
}
export const useAuthStore = defineStore('authStore', {
  state: () => {
    return {
      currentUser: null as User | null
    }
  },
  actions: {
    setCurrentUser(user: any) {
      this.currentUser = user
    }
  }
  // persist: {
  //   storage: sessionStorage,
  //   paths: ['currentUser']
  // }
})
