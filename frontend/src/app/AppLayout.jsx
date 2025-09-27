import React from "react";
import AppHeader from "./AppHeader";
import AppFooter from "./AppFooter";
import Watermark from "../shared/components/layout/Watermark";
import { CloudflareAnalytics } from "@shared/components/analytics";

/**
 * 应用布局组件
 * 负责整体页面布局和通用UI元素
 */
export default function AppLayout({ children }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Cloudflare Analytics 脚本注入 */}
      <CloudflareAnalytics />
      <Watermark />
      <AppHeader />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <AppFooter />
    </div>
  );
}
