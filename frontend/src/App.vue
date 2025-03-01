<template>
  <div id="app" class="app-container">
    <router-view v-slot="{ Component }">
      <keep-alive :exclude="['DashboardLayout']">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style lang="scss">
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.app-container {
  min-height: 100vh;
}
</style> 