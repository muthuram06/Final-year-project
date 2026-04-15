"use client"

import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"
import { AlertTriangle, X } from "lucide-react"

interface AlertPopupProps {
  message: string
  severity: "warning" | "critical"
  onDismiss: () => void
}

export function AlertPopup({ message, severity, onDismiss }: AlertPopupProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onDismiss, 300)
    }, 5000)
    return () => clearTimeout(timer)
  }, [onDismiss])

  return (
    <div
      className={cn(
        "fixed top-20 right-6 z-50 transition-all duration-300 transform",
        isVisible ? "translate-x-0 opacity-100" : "translate-x-full opacity-0"
      )}
    >
      <div
        className={cn(
          "flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-xl",
          severity === "critical"
            ? "bg-destructive/20 border-destructive/50 glow-red"
            : "bg-warning/20 border-warning/50 glow-yellow"
        )}
      >
        <AlertTriangle
          className={cn(
            "w-5 h-5 animate-pulse",
            severity === "critical" ? "text-destructive" : "text-warning"
          )}
        />
        <div>
          <p
            className={cn(
              "text-sm font-medium",
              severity === "critical" ? "text-destructive" : "text-warning"
            )}
          >
            {severity === "critical" ? "Critical Alert" : "Warning"}
          </p>
          <p className="text-xs text-muted-foreground">{message}</p>
        </div>
        <button
          onClick={() => {
            setIsVisible(false)
            setTimeout(onDismiss, 300)
          }}
          className="ml-2 text-muted-foreground hover:text-foreground transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
