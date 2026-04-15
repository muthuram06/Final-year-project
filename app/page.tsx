"use client"

import { useState, useEffect, useCallback } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { TopNavbar } from "@/components/dashboard/top-navbar"
import { VideoFeed } from "@/components/dashboard/video-feed"
import { AnalyticsCards } from "@/components/dashboard/analytics-cards"
import { LogsPanel, type LogEntry } from "@/components/dashboard/logs-panel"
import { AlertPopup } from "@/components/dashboard/alert-popup"
import {
  generateBlinkData,
  generateHeadMovementData,
  generateVoiceData,
  generateEARValue,
  generateHeadDirection,
  calculateRiskLevel,
  calculateRiskScore,
  generateMockLogs,
  generateRandomAlert,
} from "@/lib/mock-data"

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState("dashboard")
  const [currentTime, setCurrentTime] = useState("")

  // Monitoring state
  const [faceDetected, setFaceDetected] = useState(true)
  const [earValue, setEarValue] = useState(0.28)
  const [headDirection, setHeadDirection] = useState<"left" | "right" | "center" | "up" | "down">("center")
  const [deviceDetected, setDeviceDetected] = useState(false)
  const [voiceActivity, setVoiceActivity] = useState(false)

  // Analytics data
  const [blinkRate, setBlinkRate] = useState<number[]>([])
  const [headMovement, setHeadMovement] = useState<number[]>([])
  const [voiceFrequency, setVoiceFrequency] = useState<number[]>([])
  const [deviceCount, setDeviceCount] = useState(0)

  // Logs
  const [logs, setLogs] = useState<LogEntry[]>([])

  // Alerts
  const [activeAlert, setActiveAlert] = useState<{
    message: string
    severity: "warning" | "critical"
  } | null>(null)

  // Calculate derived values
  const riskLevel = calculateRiskLevel(faceDetected, earValue, headDirection, deviceDetected, voiceActivity)
  const riskScore = calculateRiskScore(faceDetected, earValue, headDirection, deviceDetected, voiceActivity)

  // Initialize data
  useEffect(() => {
    setBlinkRate(generateBlinkData(10))
    setHeadMovement(generateHeadMovementData(10))
    setVoiceFrequency(generateVoiceData(10))
    setLogs(generateMockLogs(20))
  }, [])

  // Update time
  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(
        new Date().toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
        })
      )
    }
    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Update monitoring values
      setFaceDetected(Math.random() > 0.1) // 90% of time face is detected
      setEarValue(generateEARValue())
      setHeadDirection(generateHeadDirection())
      setDeviceDetected(Math.random() < 0.05) // 5% chance of device
      setVoiceActivity(Math.random() < 0.15) // 15% chance of voice

      // Update analytics data
      setBlinkRate((prev) => [...prev.slice(1), Math.floor(Math.random() * 13) + 12])
      setHeadMovement((prev) => [...prev.slice(1), Math.floor(Math.random() * 7) + 1])
      setVoiceFrequency((prev) => [...prev.slice(1), Math.floor(Math.random() * 5)])

      // Check for alerts
      const alert = generateRandomAlert()
      if (alert && !activeAlert) {
        setActiveAlert(alert)
        // Add to logs
        setLogs((prev) => [
          {
            id: `log-${Date.now()}`,
            timestamp: new Date().toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
              hour12: false,
            }),
            eventType: alert.severity === "critical" ? "device_detected" : "head_movement",
            riskLevel: alert.severity === "critical" ? "HIGH" : "MEDIUM",
            description: alert.message,
          },
          ...prev.slice(0, 19),
        ])
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [activeAlert])

  // Update device count when device is detected
  useEffect(() => {
    if (deviceDetected) {
      setDeviceCount((prev) => prev + 1)
    }
  }, [deviceDetected])

  const handleDismissAlert = useCallback(() => {
    setActiveAlert(null)
  }, [])

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navbar */}
        <TopNavbar currentTime={currentTime} />

        {/* Content Area */}
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-[1800px] mx-auto space-y-6">
            {/* Page Header */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-foreground">Live Monitoring</h1>
                <p className="text-sm text-muted-foreground">
                  Real-time AI-powered exam proctoring dashboard
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-neon-green animate-pulse" />
                <span className="text-sm text-muted-foreground">Recording Active</span>
              </div>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              {/* Video Feed - Takes 2 columns on xl screens */}
              <div className="xl:col-span-2">
                <VideoFeed
                  riskLevel={riskLevel}
                  faceDetected={faceDetected}
                  earValue={earValue}
                  headDirection={headDirection}
                  deviceDetected={deviceDetected}
                  voiceActivity={voiceActivity}
                />
              </div>

              {/* Quick Stats Panel */}
              <div className="glass rounded-xl p-4">
                <h3 className="text-sm font-semibold text-foreground mb-4">Session Overview</h3>
                <div className="space-y-4">
                  <StatItem label="Session Duration" value="01:24:38" />
                  <StatItem label="Total Alerts" value={`${logs.filter(l => l.riskLevel === "HIGH").length}`} highlight />
                  <StatItem label="Face Visibility" value={faceDetected ? "98%" : "0%"} />
                  <StatItem label="Attention Score" value={`${100 - riskScore}%`} />
                  <StatItem label="Audio Events" value={`${voiceFrequency.filter(v => v > 2).length}`} />
                  <StatItem label="Device Incidents" value={`${deviceCount}`} highlight={deviceCount > 0} />
                </div>
              </div>
            </div>

            {/* Analytics Cards */}
            <AnalyticsCards
              blinkRate={blinkRate}
              headMovement={headMovement}
              deviceCount={deviceCount}
              voiceFrequency={voiceFrequency}
              riskScore={riskScore}
            />

            {/* Logs Panel */}
            <LogsPanel logs={logs} />
          </div>
        </main>
      </div>

      {/* Alert Popup */}
      {activeAlert && (
        <AlertPopup
          message={activeAlert.message}
          severity={activeAlert.severity}
          onDismiss={handleDismissAlert}
        />
      )}
    </div>
  )
}

function StatItem({
  label,
  value,
  highlight = false,
}: {
  label: string
  value: string
  highlight?: boolean
}) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-border/50 last:border-0">
      <span className="text-sm text-muted-foreground">{label}</span>
      <span
        className={`text-sm font-semibold ${
          highlight ? "text-destructive" : "text-foreground"
        }`}
      >
        {value}
      </span>
    </div>
  )
}
