<script setup lang="ts">
// 在这里写 JavaScript/TypeScript 代码
import { ref } from 'vue'

const msg = ref('欢迎使用学生管理系统')
</script>

<template>
  <!-- 在这里写 HTML 模板 -->
  <div>
    <h3>模板语法</h3>
    <p>{{ msg }}</p>
  </div>
</template>

<style scoped>
/* 在这里写 CSS 样式 */
h3 {
  color: #42b883;
}
</style>
