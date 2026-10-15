# 生产管理 安卓原生应用

基于 Capacitor 的原生 WebView 壳，加载在线生产计件工资管理系统：
https://kuro1016.github.io/factory-production/

- 使用系统内置 WebView 全屏运行，不依赖 Chrome、不跳浏览器。
- 数据经 Supabase 云端实时同步，多人共用。

## 自动构建
推送到 main 后，GitHub Actions 自动构建 debug APK，
在 Actions 运行页的 Artifacts 中下载 `factory-app-debug`。
