"use client";

import { useState, useEffect, useRef } from "react";
import { cn } from "@/lib/utils";
import {
  Mic,
  Eye,
  ArrowUp,
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  Smartphone,
  AlertTriangle,
  Volume2,
  Circle,
} from "lucide-react";

interface VideoFeedProps {
  riskLevel: "LOW" | "MEDIUM" | "HIGH";
  faceDetected: boolean;
  earValue: number;
  headDirection: "left" | "right" | "center" | "up" | "down";
  deviceDetected: boolean;
  voiceActivity: boolean;
}

export function VideoFeed({
  riskLevel,
  faceDetected,
  earValue,
  headDirection,
  deviceDetected,
  voiceActivity,
}: VideoFeedProps) {
  const [isRecording] = useState(true);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // 🎥 CAMERA START
  useEffect(() => {
    let stream: MediaStream;

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Camera error:", err);
      }
    };

    startCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);
  // 🎥 CAMERA END

  const riskColors = {
    LOW: { bg: "bg-neon-green/20", text: "text-neon-green", glow: "glow-green" },
    MEDIUM: { bg: "bg-warning/20", text: "text-warning", glow: "glow-yellow" },
    HIGH: { bg: "bg-destructive/20", text: "text-destructive", glow: "glow-red" },
  };

  const headIcons = {
    left: ArrowLeft,
    right: ArrowRight,
    center: Circle,
    up: ArrowUp,
    down: ArrowDown,
  };

  const HeadIcon = headIcons[headDirection];

  return (
    <div className="glass rounded-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div
              className={cn(
                "w-2 h-2 rounded-full",
                isRecording ? "bg-destructive animate-pulse" : "bg-muted"
              )}
            />
            <span className="text-sm font-medium text-foreground">
              Live Feed
            </span>
          </div>
          <span className="text-xs text-muted-foreground">
            • Exam Session #2847
          </span>
        </div>

        {/* Risk Badge */}
        <div
          className={cn(
            "px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5",
            riskColors[riskLevel].bg,
            riskColors[riskLevel].text,
            riskColors[riskLevel].glow
          )}
        >
          <AlertTriangle className="w-3 h-3" />
          {riskLevel} RISK
        </div>
      </div>

      {/* Video Area */}
      <div className="relative aspect-video bg-black">

        {/* 🎥 REAL CAMERA */}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="absolute inset-0 w-full h-full object-cover"
        />

        {/* Face Detection Box */}
        {faceDetected && (
          <div className="absolute inset-10 border-2 border-neon-cyan rounded-lg animate-pulse pointer-events-none" />
        )}

        {/* Device Detection */}
        {deviceDetected && (
          <div className="absolute top-4 right-4 px-3 py-2 bg-destructive/20 border border-destructive/50 rounded-lg flex items-center gap-2 animate-pulse">
            <Smartphone className="w-4 h-4 text-destructive" />
            <span className="text-xs font-medium text-destructive">
              Device Detected
            </span>
          </div>
        )}

        {/* Bottom Indicators */}
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <div className="flex items-center justify-between">

            {/* LEFT */}
            <div className="flex items-center gap-3">
              <IndicatorBadge
                icon={Eye}
                label="Face"
                value={faceDetected ? "Detected" : "Not Found"}
                active={faceDetected}
                variant={faceDetected ? "success" : "danger"}
              />

              <IndicatorBadge
                icon={Eye}
                label="EAR"
                value={earValue.toFixed(2)}
                active={earValue > 0.2}
                variant={earValue > 0.2 ? "success" : "warning"}
              />
            </div>

            {/* RIGHT */}
            <div className="flex items-center gap-3">
              <div className="glass px-3 py-2 rounded-lg flex items-center gap-2">
                <HeadIcon
                  className={cn(
                    "w-4 h-4",
                    headDirection === "center"
                      ? "text-neon-green"
                      : "text-warning"
                  )}
                />
                <span className="text-xs text-foreground capitalize">
                  {headDirection}
                </span>
              </div>

              <IndicatorBadge
                icon={voiceActivity ? Volume2 : Mic}
                label="Audio"
                value={voiceActivity ? "Active" : "Silent"}
                active={voiceActivity}
                variant={voiceActivity ? "warning" : "success"}
              />
            </div>
          </div>
        </div>

        {/* Corner Borders */}
        <div className="absolute top-4 left-4 w-8 h-8 border-l-2 border-t-2 border-primary/50" />
        <div className="absolute top-4 right-4 w-8 h-8 border-r-2 border-t-2 border-primary/50" />
        <div className="absolute bottom-20 left-4 w-8 h-8 border-l-2 border-b-2 border-primary/50" />
        <div className="absolute bottom-20 right-4 w-8 h-8 border-r-2 border-b-2 border-primary/50" />
      </div>
    </div>
  );
}

function IndicatorBadge({
  icon: Icon,
  label,
  value,
  active,
  variant,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  active: boolean;
  variant: "success" | "warning" | "danger";
}) {
  const variantStyles = {
    success: "text-neon-green bg-neon-green/10 border-neon-green/30",
    warning: "text-warning bg-warning/10 border-warning/30",
    danger: "text-destructive bg-destructive/10 border-destructive/30",
  };

  return (
    <div
      className={cn(
        "px-3 py-2 rounded-lg flex items-center gap-2 border",
        variantStyles[variant]
      )}
    >
      <Icon className="w-4 h-4" />
      <div className="text-xs">
        <span className="text-muted-foreground">{label}: </span>
        <span className="font-medium">{value}</span>
      </div>
    </div>
  );
}