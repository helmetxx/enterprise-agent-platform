<template>
  <div class="avatar-container">
    <el-avatar :size="100" :src="userStore.user?.avatar || config.defaultAvatar" />
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { config } from '@/config'
</script> 