"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { Search, Filter, ChevronDown, AlertTriangle, Info, CheckCircle } from "lucide-react"

export interface LogEntry {
  id: string
  timestamp: string
  eventType: "face_detection" | "blink_anomaly" | "head_movement" | "device_detected" | "voice_detected" | "system"
  riskLevel: "LOW" | "MEDIUM" | "HIGH"
  description: string
}

interface LogsPanelProps {
  logs: LogEntry[]
  expanded?: boolean
}

export function LogsPanel({ logs, expanded = false }: LogsPanelProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [filterRisk, setFilterRisk] = useState<"ALL" | "LOW" | "MEDIUM" | "HIGH">("ALL")
  const [isExpanded, setIsExpanded] = useState(expanded)

  const filteredLogs = logs.filter((log) => {
    const matchesSearch =
      log.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.eventType.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRisk = filterRisk === "ALL" || log.riskLevel === filterRisk
    return matchesSearch && matchesRisk
  })

  const eventTypeIcons = {
    face_detection: "👤",
    blink_anomaly: "👁️",
    head_movement: "↔️",
    device_detected: "📱",
    voice_detected: "🔊",
    system: "⚙️",
  }

  const riskColors = {
    LOW: { bg: "bg-neon-green/10", text: "text-neon-green", border: "border-neon-green/30" },
    MEDIUM: { bg: "bg-warning/10", text: "text-warning", border: "border-warning/30" },
    HIGH: { bg: "bg-destructive/10", text: "text-destructive", border: "border-destructive/30" },
  }

  return (
    <div className={cn(
      "glass rounded-xl overflow-hidden transition-all duration-300",
      isExpanded ? "h-[500px]" : "h-[300px]"
    )}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-foreground">Activity Logs</h3>
          <span className="px-2 py-0.5 bg-primary/20 rounded-full text-xs text-primary">
            {filteredLogs.length} events
          </span>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          <ChevronDown className={cn("w-4 h-4 transition-transform", isExpanded && "rotate-180")} />
        </button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-border bg-secondary/30">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search logs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full h-8 pl-10 pr-4 bg-input rounded-lg text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-muted-foreground" />
          {["ALL", "LOW", "MEDIUM", "HIGH"].map((risk) => (
            <button
              key={risk}
              onClick={() => setFilterRisk(risk as typeof filterRisk)}
              className={cn(
                "px-2 py-1 rounded text-xs font-medium transition-all",
                filterRisk === risk
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-muted-foreground hover:text-foreground"
              )}
            >
              {risk}
            </button>
          ))}
        </div>
      </div>

      {/* Logs Table */}
      <div className="overflow-auto h-[calc(100%-110px)]">
        <table className="w-full">
          <thead className="sticky top-0 bg-card/90 backdrop-blur-sm">
            <tr className="text-left text-xs text-muted-foreground border-b border-border">
              <th className="px-4 py-2 font-medium">Timestamp</th>
              <th className="px-4 py-2 font-medium">Event Type</th>
              <th className="px-4 py-2 font-medium">Risk Level</th>
              <th className="px-4 py-2 font-medium">Description</th>
            </tr>
          </thead>
          <tbody>
            {filteredLogs.map((log) => (
              <tr
                key={log.id}
                className={cn(
                  "border-b border-border/50 hover:bg-secondary/30 transition-colors text-sm",
                  log.riskLevel === "HIGH" && "bg-destructive/5"
                )}
              >
                <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                  {log.timestamp}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span>{eventTypeIcons[log.eventType]}</span>
                    <span className="capitalize text-foreground">
                      {log.eventType.replace(/_/g, " ")}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span
                    className={cn(
                      "px-2 py-0.5 rounded-full text-xs font-medium border",
                      riskColors[log.riskLevel].bg,
                      riskColors[log.riskLevel].text,
                      riskColors[log.riskLevel].border
                    )}
                  >
                    {log.riskLevel}
                  </span>
                </td>
                <td className={cn(
                  "px-4 py-3",
                  log.riskLevel === "HIGH" ? "text-destructive" : "text-foreground"
                )}>
                  {log.description}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
