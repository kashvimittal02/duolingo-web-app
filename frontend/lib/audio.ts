// Lightweight client-side Web Audio & Web Speech synthesis utilities
// 100% self-contained: zero external audio assets, zero backend requests, fails gracefully.

class SoundEffects {
  private ctx: AudioContext | null = null;
  private muted: boolean = false;

  constructor() {
    if (typeof window !== "undefined") {
      try {
        const stored = localStorage.getItem("duo_sound_muted");
        if (stored !== null) {
          this.muted = stored === "true";
        }
      } catch {
        // Suppress storage errors
      }
    }
  }

  isMuted(): boolean {
    return this.muted;
  }

  setMuted(mute: boolean): void {
    this.muted = mute;
    if (typeof window !== "undefined") {
      try {
        localStorage.setItem("duo_sound_muted", String(mute));
      } catch {
        // Suppress storage errors
      }
    }
  }

  toggleMute(): boolean {
    this.setMuted(!this.muted);
    return this.muted;
  }

  private getContext(): AudioContext | null {
    if (this.muted) return null;
    if (typeof window === "undefined") return null;
    try {
      if (!this.ctx) {
        const AudioCtx =
          window.AudioContext || (window as any).webkitAudioContext;
        if (AudioCtx) {
          this.ctx = new AudioCtx();
        }
      }
      if (this.ctx && this.ctx.state === "suspended") {
        this.ctx.resume().catch(() => {});
      }
      return this.ctx;
    } catch {
      return null;
    }
  }

  // Bright ascending two-tone Duolingo-inspired chime (C5 -> G5)
  playCorrect() {
    if (this.muted) return;
    try {
      const ctx = this.getContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      // First note: C5 (523.25 Hz)
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(523.25, now);
      gain1.gain.setValueAtTime(0.2, now);
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc1.connect(gain1);
      gain1.connect(ctx.destination);
      osc1.start(now);
      osc1.stop(now + 0.18);

      // Second note: G5 (783.99 Hz)
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = "sine";
      osc2.frequency.setValueAtTime(783.99, now + 0.1);
      gain2.gain.setValueAtTime(0.25, now + 0.1);
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
      osc2.connect(gain2);
      gain2.connect(ctx.destination);
      osc2.start(now + 0.1);
      osc2.stop(now + 0.32);
    } catch {
      // Audio errors are safely suppressed
    }
  }

  // Gentle low descending buzzer for incorrect answers
  playIncorrect() {
    if (this.muted) return;
    try {
      const ctx = this.getContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(260, now);
      osc.frequency.linearRampToValueAtTime(170, now + 0.22);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.25);
    } catch {
      // Audio errors are safely suppressed
    }
  }

  // Festive triumph fanfare chord for lesson completion
  playLessonComplete() {
    if (this.muted) return;
    try {
      const ctx = this.getContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      // Arpeggiated C major triad: C5 (523.25), E5 (659.25), G5 (783.99), C6 (1046.5)
      const notes = [
        { freq: 523.25, time: 0.0, dur: 0.25 },
        { freq: 659.25, time: 0.08, dur: 0.25 },
        { freq: 783.99, time: 0.16, dur: 0.35 },
        { freq: 1046.5, time: 0.25, dur: 0.55 },
      ];

      notes.forEach(({ freq, time, dur }) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, now + time);
        gain.gain.setValueAtTime(0.18, now + time);
        gain.gain.exponentialRampToValueAtTime(0.001, now + time + dur);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + time);
        osc.stop(now + time + dur);
      });
    } catch {
      // Audio errors are safely suppressed
    }
  }

  // Soft subtle click for tile placement
  playTap() {
    if (this.muted) return;
    try {
      const ctx = this.getContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(700, now);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.03);
    } catch {
      // Audio errors are safely suppressed
    }
  }
}

export const sounds = new SoundEffects();

// Browser Web Speech API (speechSynthesis) for Spanish pronunciation
export function speakSpanish(text: string): void {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return;
  }
  try {
    // Cancel any previous active speech
    window.speechSynthesis.cancel();

    // Clean up blank placeholders like "___"
    const cleaned = text.replace(/___+/g, " ").trim();
    if (!cleaned) return;

    const utterance = new SpeechSynthesisUtterance(cleaned);
    utterance.lang = "es-ES";
    utterance.rate = 0.9; // Clear learning pace

    // Prefer Spanish voice if available
    const voices = window.speechSynthesis.getVoices();
    const esVoice = voices.find(
      (v) =>
        v.lang === "es-ES" ||
        v.lang.startsWith("es-") ||
        v.lang.startsWith("es_") ||
        v.lang.toLowerCase().includes("spanish")
    );
    if (esVoice) {
      utterance.voice = esVoice;
    }

    window.speechSynthesis.speak(utterance);
  } catch (err) {
    // Non-blocking fallback
    console.warn("Speech synthesis unavailable:", err);
  }
}
