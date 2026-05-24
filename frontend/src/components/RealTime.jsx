import React, { useEffect, useRef, useState } from "react";

const RealTime = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const beepRef = useRef(null);
  const [detections, setDetections] = useState([]);
  const [alertActive, setAlertActive] = useState(false);

  // store last alert time per label
  const lastAlertTimes = useRef({});

  useEffect(() => {
    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      videoRef.current.srcObject = stream;
    });

    // Initialize beep sound
    beepRef.current = new Audio("/beep.mp3");
    beepRef.current.volume = 0.8;

    // Send a frame every second
    const interval = setInterval(() => {
      captureAndSendFrame();
    }, 500);

    return () => clearInterval(interval);
  }, []);

  // Capture frame from video and send to FastAPI
  async function captureAndSendFrame() {
    const video = videoRef.current;
    if (!video || !video.videoWidth) return;

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise((res) => canvas.toBlob(res, "image/jpeg"));
    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");

    try {
      const res = await fetch("http://localhost:8000/detect", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (data.detections) {
        setDetections(data.detections);
        drawDetections(data.detections);
        checkForAlert(data.detections);
      }
    } catch (err) {
      console.error("Detection error:", err);
    }
  }

  // Check for alerts (only beep once per object type every few seconds)
  function checkForAlert(detections) {
    const now = Date.now();
    let alert = false;

    for (const d of detections) {
      const label = d.name.toLowerCase();

      const isDanger =
        label.includes("pothole") ||
        label.includes("speedbreaker") ||
        (label.includes("person") && d.conf > 0.7);

      if (isDanger) {
        alert = true;

        const lastTime = lastAlertTimes.current[label] || 0;

        // ✅ Beep only if 5 seconds passed since last alert for same label
        if (now - lastTime > 5000) {
          playBeep();
          lastAlertTimes.current[label] = now;
        }
      }
    }

    setAlertActive(alert);
  }

  // Play beep sound
  function playBeep() {
    if (beepRef.current) {
      beepRef.current.currentTime = 0;
      beepRef.current
        .play()
        .then(() => console.log("Beep!"))
        .catch((err) => console.warn("Audio blocked until user click:", err));
    }
  }

  // Draw bounding boxes
  function drawDetections(dets) {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const video = videoRef.current;

    if (!canvas || !ctx || !video.videoWidth) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const d of dets) {
      ctx.strokeStyle = "lime";
      ctx.lineWidth = 2;
      ctx.strokeRect(d.x1, d.y1, d.x2 - d.x1, d.y2 - d.y1);

      ctx.fillStyle = "rgba(0, 255, 0, 0.6)";
      ctx.font = "14px Arial";
      ctx.fillText(`${d.name} ${d.conf.toFixed(2)}`, d.x1 + 4, d.y1 - 4);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center bg-black min-h-screen">
      <div className="relative">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className={`rounded-xl transition-all duration-200 ${
            alertActive ? "ring-4 ring-red-600 animate-pulse" : ""
          }`}
        />
        <canvas ref={canvasRef} className="absolute top-0 left-0" />
      </div>

      <button
        onClick={() =>
          beepRef.current
            .play()
            .then(() => console.log("Sound enabled"))
            .catch(() => alert("Click once to allow sound playback!"))
        }
        className="mt-3 px-4 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition"
      >
        Enable Sound 🔊
      </button>

      <p className="text-white mt-3 text-sm opacity-70">
        Real-time YOLOv8 Detection (1 beep per object type / 10 sec cooldown)
      </p>
    </div>
  );
};

export default RealTime;