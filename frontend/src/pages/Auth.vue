<template>
  <div class="w-screen h-screen p-5">
    <div class="flex flex-row">
      <div class="w-[50%] min-h-[350px] mr-6 rounded py-5 px-5 bg-slate-100">
        <div class="text-xl underline mb-5">Register Form</div>
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-width="135px"
          label-position="left"
        >
          <el-form-item label="Username" prop="username">
            <el-input v-model="registerForm.username"></el-input>
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="registerForm.password"></el-input>
          </el-form-item>
          <el-form-item label="Confirm Password" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword"></el-input>
          </el-form-item>

          <div class="text-right">
            <el-button type="primary" @click="register"> Register </el-button>
          </div>
        </el-form>
      </div>
      <div class="w-[50%] min-h-[350px] ml-6 rounded py-5 px-5 bg-slate-100">
        <div class="text-xl underline mb-5">Login Form</div>
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="135px"
          label-position="left"
        >
          <el-form-item label="Username" prop="username">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="loginForm.password"></el-input>
          </el-form-item>

          <div class="text-right">
            <el-button type="primary" @click="login"> Login </el-button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosError } from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores'
import { ElMessage, FormRules, FormInstance } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const registerFormRef = ref<FormInstance>()
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})
const registerRules = ref<FormRules>({
  username: [{ required: true, min: 4 }],
  password: [{ required: true, min: 6 }],
  confirmPassword: [
    { required: true },
    {
      validator: (rule: any, value: any, callback: any) => {
        if (!value) return callback(new Error('Value is required'))

        if (value == registerForm.value.password) {
          return callback()
        }

        return callback(new Error('Passwords do not match'))
      }
    }
  ]
})

const loginFormRef = ref<FormInstance>()
const loginForm = ref({
  username: '',
  password: ''
})
const loginRules = ref<FormRules>({
  username: [{ required: true }],
  password: [{ required: true }]
})

const register = () => {
  registerFormRef.value?.validate((isValid) => {
    if (isValid) {
      const { username, password } = registerForm.value
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/auth/register',
        data: {
          username: username,
          password: password
        },
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-type': 'application/json'
        }
      })
        .then((response) => {
          if (response.status != 200) {
            ElMessage({ type: 'error', message: 'Something went wrong!' })
            return
          }

          ElMessage({ type: 'success', message: 'User register success!' })

          registerFormRef.value?.resetFields()
        })
        .catch((error) => {
          if (error?.response?.data) {
            ElMessage({ type: 'error', message: error.response.data as string })
          }

          ElMessage({
            type: 'error',
            message: error.message || 'Register user error!'
          })
        })
    }
  })
}

const login = () => {
  loginFormRef.value?.validate((isValid) => {
    if (isValid) {
      const { username, password } = loginForm.value
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/auth/login',
        data: {
          username: username,
          password: password
        },
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-type': 'application/json'
        }
      })
        .then((response) => {
          if (response.status != 200) {
            ElMessage({ type: 'error', message: 'Something went wrong!' })
            return
          }

          ElMessage({ type: 'success', message: 'You are logged in!' })

          authStore.setCurrentUser(response.data)
          // go dashboard
          router.push('/')
        })
        .catch((error: AxiosError) => {
          if (error?.response?.data) {
            ElMessage({ type: 'error', message: error.response.data as string })
          }
          ElMessage({
            type: 'error',
            message: error.message || 'Login error!'
          })
        })
    }
  })
}
</script>
