import type { LogEntry } from "@/components/dashboard/logs-panel"

// API Placeholders - Replace with real API calls
export const API_ENDPOINTS = {
  VIDEO_STREAM: "/api/video-stream",
  RISK_SCORE: "/api/risk-score",
  LOGS: "/api/logs",
} as const

// Generate random number within range
function randomInRange(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

// Generate random float
function randomFloat(min: number, max: number): number {
  return Math.random() * (max - min) + min
}

// Generate mock blink rate data
export function generateBlinkData(count: number = 10): number[] {
  return Array.from({ length: count }, () => randomInRange(12, 25))
}

// Generate mock head movement data
export function generateHeadMovementData(count: number = 10): number[] {
  return Array.from({ length: count }, () => randomInRange(1, 8))
}

// Generate mock voice frequency data
export function generateVoiceData(count: number = 10): number[] {
  return Array.from({ length: count }, () => randomInRange(0, 5))
}

// Generate random EAR value
export function generateEARValue(): number {
  return randomFloat(0.15, 0.35)
}

// Generate random head direction
export function generateHeadDirection(): "left" | "right" | "center" | "up" | "down" {
  const directions: ("left" | "right" | "center" | "up" | "down")[] = [
    "center", "center", "center", "center", // More likely to be center
    "left", "right", "up", "down"
  ]
  return directions[randomInRange(0, directions.length - 1)]
}

// Calculate risk level based on metrics
export function calculateRiskLevel(
  faceDetected: boolean,
  earValue: number,
  headDirection: string,
  deviceDetected: boolean,
  voiceActivity: boolean
): "LOW" | "MEDIUM" | "HIGH" {
  let riskScore = 0

  if (!faceDetected) riskScore += 40
  if (earValue < 0.2) riskScore += 20
  if (headDirection !== "center") riskScore += 15
  if (deviceDetected) riskScore += 50
  if (voiceActivity) riskScore += 25

  if (riskScore >= 60) return "HIGH"
  if (riskScore >= 30) return "MEDIUM"
  return "LOW"
}

// Calculate numeric risk score
export function calculateRiskScore(
  faceDetected: boolean,
  earValue: number,
  headDirection: string,
  deviceDetected: boolean,
  voiceActivity: boolean
): number {
  let score = 0

  if (!faceDetected) score += 30
  if (earValue < 0.2) score += 15
  if (headDirection !== "center") score += 10
  if (deviceDetected) score += 35
  if (voiceActivity) score += 20

  return Math.min(score, 100)
}

// Generate mock log entries
export function generateMockLogs(count: number = 20): LogEntry[] {
  const eventTypes: LogEntry["eventType"][] = [
    "face_detection",
    "blink_anomaly",
    "head_movement",
    "device_detected",
    "voice_detected",
    "system",
  ]

  const descriptions: Record<LogEntry["eventType"], string[]> = {
    face_detection: [
      "Face detected in frame",
      "Face lost - looking away from screen",
      "Multiple faces detected in frame",
      "Face detection confidence: 98%",
    ],
    blink_anomaly: [
      "Unusual blink pattern detected",
      "Blink rate normal",
      "Extended eye closure detected",
      "EAR value dropped below threshold",
    ],
    head_movement: [
      "Head turned left",
      "Head turned right",
      "Looking down at desk",
      "Frequent head movements detected",
    ],
    device_detected: [
      "Mobile phone detected in frame",
      "Secondary device visible",
      "Smartwatch detected on wrist",
      "Electronic device in peripheral view",
    ],
    voice_detected: [
      "Audio activity detected",
      "Voice input recognized",
      "Background conversation detected",
      "Ambient noise spike",
    ],
    system: [
      "Monitoring session started",
      "Connection quality: Excellent",
      "Auto-save checkpoint created",
      "System health check passed",
    ],
  }

  const now = new Date()

  return Array.from({ length: count }, (_, i) => {
    const eventType = eventTypes[randomInRange(0, eventTypes.length - 1)]
    const descList = descriptions[eventType]
    const description = descList[randomInRange(0, descList.length - 1)]

    // Determine risk level based on event type and description
    let riskLevel: LogEntry["riskLevel"] = "LOW"
    if (eventType === "device_detected") riskLevel = "HIGH"
    else if (eventType === "voice_detected" && description.includes("conversation")) riskLevel = "HIGH"
    else if (description.includes("lost") || description.includes("Multiple")) riskLevel = "MEDIUM"
    else if (description.includes("anomaly") || description.includes("unusual")) riskLevel = "MEDIUM"

    const timestamp = new Date(now.getTime() - i * randomInRange(5000, 30000))

    return {
      id: `log-${i}`,
      timestamp: timestamp.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      }),
      eventType,
      riskLevel,
      description,
    }
  })
}

// Generate random alert
export function generateRandomAlert(): { message: string; severity: "warning" | "critical" } | null {
  const random = Math.random()
  if (random < 0.1) {
    return {
      message: "Mobile device detected in frame!",
      severity: "critical",
    }
  }
  if (random < 0.2) {
    return {
      message: "Student looking away from screen",
      severity: "warning",
    }
  }
  return null
}
