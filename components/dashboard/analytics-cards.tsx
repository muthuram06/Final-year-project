"use client"

import { cn } from "@/lib/utils"
import {
  Eye,
  Move,
  Smartphone,
  Volume2,
  Shield,
  TrendingUp,
  TrendingDown,
} from "lucide-react"
import {
  LineChart,
  Line,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts"

interface AnalyticsCardsProps {
  blinkRate: number[]
  headMovement: number[]
  deviceCount: number
  voiceFrequency: number[]
  riskScore: number
}

export function AnalyticsCards({
  blinkRate,
  headMovement,
  deviceCount,
  voiceFrequency,
  riskScore,
}: AnalyticsCardsProps) {
  const chartData = blinkRate.map((value, index) => ({
    blink: value,
    head: headMovement[index] || 0,
    voice: voiceFrequency[index] || 0,
  }))

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
      {/* Blink Rate Card */}
      <AnalyticsCard
        title="Blink Rate"
        value={`${blinkRate[blinkRate.length - 1] || 0}`}
        unit="bpm"
        icon={Eye}
        trend={blinkRate[blinkRate.length - 1] > blinkRate[blinkRate.length - 2] ? "up" : "down"}
        color="primary"
      >
        <ResponsiveContainer width="100%" height={60}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="blinkGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.65 0.2 250)" stopOpacity={0.3} />
                <stop offset="100%" stopColor="oklch(0.65 0.2 250)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="blink"
              stroke="oklch(0.65 0.2 250)"
              fill="url(#blinkGradient)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </AnalyticsCard>

      {/* Head Movement Card */}
      <AnalyticsCard
        title="Head Movement"
        value={`${headMovement[headMovement.length - 1] || 0}`}
        unit="freq"
        icon={Move}
        trend={headMovement[headMovement.length - 1] > headMovement[headMovement.length - 2] ? "up" : "down"}
        color="cyan"
      >
        <ResponsiveContainer width="100%" height={60}>
          <LineChart data={chartData}>
            <Line
              type="monotone"
              dataKey="head"
              stroke="oklch(0.75 0.15 195)"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </AnalyticsCard>

      {/* Device Detection Card */}
      <AnalyticsCard
        title="Device Detection"
        value={`${deviceCount}`}
        unit="count"
        icon={Smartphone}
        trend={deviceCount > 0 ? "up" : "down"}
        color={deviceCount > 0 ? "destructive" : "green"}
      >
        <div className="flex items-end justify-center h-[60px] gap-1">
          {[0, 1, 2, 0, deviceCount > 0 ? 3 : 0, 1, 0].map((height, i) => (
            <div
              key={i}
              className={cn(
                "w-4 rounded-t transition-all duration-500",
                height > 0 ? "bg-destructive/60" : "bg-muted/30"
              )}
              style={{ height: `${Math.max(height * 15, 4)}px` }}
            />
          ))}
        </div>
      </AnalyticsCard>

      {/* Voice Detection Card */}
      <AnalyticsCard
        title="Voice Activity"
        value={`${voiceFrequency[voiceFrequency.length - 1] || 0}`}
        unit="freq"
        icon={Volume2}
        trend={voiceFrequency[voiceFrequency.length - 1] > 2 ? "up" : "down"}
        color={voiceFrequency[voiceFrequency.length - 1] > 2 ? "warning" : "green"}
      >
        <ResponsiveContainer width="100%" height={60}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="voiceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.75 0.18 80)" stopOpacity={0.3} />
                <stop offset="100%" stopColor="oklch(0.75 0.18 80)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="voice"
              stroke="oklch(0.75 0.18 80)"
              fill="url(#voiceGradient)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </AnalyticsCard>

      {/* Risk Score Card */}
      <AnalyticsCard
        title="Risk Score"
        value=""
        unit=""
        icon={Shield}
        trend={riskScore > 50 ? "up" : "down"}
        color={riskScore > 70 ? "destructive" : riskScore > 40 ? "warning" : "green"}
      >
        <div className="flex items-center justify-center h-[60px]">
          <div className="relative w-16 h-16">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
              <circle
                cx="18"
                cy="18"
                r="15.5"
                fill="none"
                stroke="oklch(0.15 0.01 260)"
                strokeWidth="3"
              />
              <circle
                cx="18"
                cy="18"
                r="15.5"
                fill="none"
                stroke={
                  riskScore > 70
                    ? "oklch(0.55 0.22 25)"
                    : riskScore > 40
                    ? "oklch(0.75 0.18 80)"
                    : "oklch(0.75 0.2 145)"
                }
                strokeWidth="3"
                strokeDasharray={`${riskScore} 100`}
                strokeLinecap="round"
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={cn(
                "text-lg font-bold",
                riskScore > 70 ? "text-destructive" : riskScore > 40 ? "text-warning" : "text-neon-green"
              )}>
                {riskScore}
              </span>
            </div>
          </div>
        </div>
      </AnalyticsCard>
    </div>
  )
}

function AnalyticsCard({
  title,
  value,
  unit,
  icon: Icon,
  trend,
  color,
  children,
}: {
  title: string
  value: string
  unit: string
  icon: React.ElementType
  trend: "up" | "down"
  color: "primary" | "cyan" | "green" | "warning" | "destructive"
  children: React.ReactNode
}) {
  const colorStyles = {
    primary: "text-primary",
    cyan: "text-neon-cyan",
    green: "text-neon-green",
    warning: "text-warning",
    destructive: "text-destructive",
  }

  return (
    <div className="glass rounded-xl p-4 glass-hover group cursor-pointer">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Icon className={cn("w-4 h-4", colorStyles[color])} />
          <span className="text-xs font-medium text-muted-foreground">{title}</span>
        </div>
        {trend === "up" ? (
          <TrendingUp className={cn("w-3 h-3", color === "green" || color === "cyan" ? "text-neon-green" : "text-destructive")} />
        ) : (
          <TrendingDown className="w-3 h-3 text-neon-green" />
        )}
      </div>
      
      {value && (
        <div className="mb-2">
          <span className={cn("text-2xl font-bold", colorStyles[color])}>{value}</span>
          <span className="text-xs text-muted-foreground ml-1">{unit}</span>
        </div>
      )}

      <div className="opacity-80 group-hover:opacity-100 transition-opacity">
        {children}
      </div>
    </div>
  )
}
