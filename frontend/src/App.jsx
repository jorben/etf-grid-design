import React from "react";
import { HelmetProvider } from "react-helmet-async";
import AppRouter from "./app/AppRouter";
import AppLayout from "./app/AppLayout";
import "./App.css";

/**
 * 主应用组件 - 简化版本
 * 仅负责提供全局上下文和渲染应用布局
 */
function App() {
  return (
    <HelmetProvider>
      <AppLayout>
        <AppRouter />
      </AppLayout>
    </HelmetProvider>
  );
}

export default App;
