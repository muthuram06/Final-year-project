"use client"

import { Bell, Search, User, Activity, Wifi, HardDrive } from "lucide-react"
import { cn } from "@/lib/utils"

interface TopNavbarProps {
  currentTime: string
}

export function TopNavbar({ currentTime }: TopNavbarProps) {
  return (
    <header className="h-16 glass border-b border-border flex items-center justify-between px-6">
      {/* Left: Search */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search exams, students..."
            className="w-64 h-9 pl-10 pr-4 bg-input rounded-lg text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
          />
        </div>
      </div>

      {/* Center: System Status */}
      <div className="flex items-center gap-6">
        <StatusIndicator icon={Activity} label="CPU" value="24%" status="good" />
        <StatusIndicator icon={HardDrive} label="Memory" value="67%" status="good" />
        <StatusIndicator icon={Wifi} label="Network" value="Stable" status="good" />
      </div>

      {/* Right: Time, Notifications, Profile */}
      <div className="flex items-center gap-4">
        <div className="text-sm text-muted-foreground font-mono">
          {currentTime}
        </div>
        
        <button className="relative w-9 h-9 rounded-lg bg-secondary flex items-center justify-center hover:bg-secondary/80 transition-colors">
          <Bell className="w-4 h-4 text-foreground" />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-destructive rounded-full text-[10px] font-medium flex items-center justify-center text-destructive-foreground">
            3
          </span>
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-border">
          <div className="text-right">
            <p className="text-sm font-medium text-foreground">Admin User</p>
            <p className="text-xs text-muted-foreground">Supervisor</p>
          </div>
          <div className="w-9 h-9 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30">
            <User className="w-5 h-5 text-primary" />
          </div>
        </div>
      </div>
    </header>
  )
}

function StatusIndicator({
  icon: Icon,
  label,
  value,
  status,
}: {
  icon: React.ElementType
  label: string
  value: string
  status: "good" | "warning" | "critical"
}) {
  const statusColors = {
    good: "text-neon-green",
    warning: "text-warning",
    critical: "text-destructive",
  }

  return (
    <div className="flex items-center gap-2">
      <Icon className={cn("w-4 h-4", statusColors[status])} />
      <div className="text-xs">
        <span className="text-muted-foreground">{label}: </span>
        <span className={cn("font-medium", statusColors[status])}>{value}</span>
      </div>
    </div>
  )
}
