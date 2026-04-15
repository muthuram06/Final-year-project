"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Monitor,
  FileText,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  Shield,
} from "lucide-react"

interface SidebarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "monitoring", label: "Live Monitoring", icon: Monitor },
  { id: "logs", label: "Logs", icon: FileText },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
  { id: "settings", label: "Settings", icon: Settings },
]

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        "h-screen bg-sidebar border-r border-sidebar-border flex flex-col transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
    >
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-sidebar-border">
        <div className={cn("flex items-center gap-3", collapsed && "justify-center w-full")}>
          <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center glow-blue">
            <Shield className="w-5 h-5 text-primary" />
          </div>
          {!collapsed && (
            <span className="font-semibold text-sidebar-foreground tracking-tight">
              ProctorAI
            </span>
          )}
        </div>
        <button
          onClick={() => setCollapsed(!collapsed)}
          className={cn(
            "w-6 h-6 rounded-md flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-sidebar-accent transition-colors",
            collapsed && "hidden"
          )}
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = activeTab === item.id
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200",
                collapsed && "justify-center px-0",
                isActive
                  ? "bg-primary/10 text-primary border border-primary/20 glow-blue"
                  : "text-muted-foreground hover:text-foreground hover:bg-sidebar-accent"
              )}
            >
              <Icon className={cn("w-5 h-5 flex-shrink-0", isActive && "text-primary")} />
              {!collapsed && (
                <span className="text-sm font-medium">{item.label}</span>
              )}
            </button>
          )
        })}
      </nav>

      {/* Collapse Toggle */}
      {collapsed && (
        <div className="py-4 px-2 border-t border-sidebar-border">
          <button
            onClick={() => setCollapsed(false)}
            className="w-full flex items-center justify-center py-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Status Indicator */}
      <div className={cn(
        "p-4 border-t border-sidebar-border",
        collapsed && "px-2"
      )}>
        <div className={cn(
          "flex items-center gap-2",
          collapsed && "justify-center"
        )}>
          <div className="w-2 h-2 rounded-full bg-neon-green animate-pulse" />
          {!collapsed && (
            <span className="text-xs text-muted-foreground">System Online</span>
          )}
        </div>
      </div>
    </aside>
  )
}
