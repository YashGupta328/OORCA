import { ChevronLeft, ChevronRight, Play, Pause, FastForward, SkipBack, SkipForward } from 'lucide-react';
import type { SpillFrame } from '@/types';

interface TimelineProps {
  frames: SpillFrame[];
  currentIndex: number;
  onFrameChange: (index: number) => void;
  disabled: boolean;
}

export function Timeline({ frames, currentIndex, onFrameChange, disabled }: TimelineProps) {
  if (frames.length === 0) {
    return (
      <div className="p-4 text-center text-dark-text-muted text-sm border-t border-dark-border">
        Run a simulation to enable timeline
      </div>
    );
  }

  const times = frames.map(f => f.time_hours);
  const minTime = Math.min(...times);
  const maxTime = Math.max(...times);
  const timeRange = maxTime - minTime;

  const getPosition = (time: number) => {
    if (timeRange === 0) return 50;
    return ((time - minTime) / timeRange) * 100;
  };

  const isPlaying = false; // Could add animation later

  return (
    <div className="p-4 border-t border-dark-border animate-in">
      <div className="space-y-3">
        {/* Timeline Track */}
        <div className="relative h-8">
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-dark-border -translate-y-1/2" />
          
          {/* Time markers */}
          {times.map((time, i) => (
            <button
              key={time}
              onClick={() => !disabled && onFrameChange(i)}
              disabled={disabled}
              className={`absolute top-0 transform -translate-x-1/2 transition-all duration-200 ${
                i === currentIndex
                  ? 'text-marine-400 font-semibold scale-110'
                  : 'text-dark-text-muted hover:text-dark-text'
              }`}
              style={{ left: `${getPosition(time)}%` }}
            >
              <div className="flex flex-col items-center">
                <div className={`w-2 h-2 rounded-full transition-all ${
                  i === currentIndex ? 'bg-marine-400' : 'bg-dark-border'
                }`} />
                <span className="text-[10px] font-mono mt-1 whitespace-nowrap">{time}h</span>
              </div>
            </button>
          ))}

          {/* Current position indicator */}
          <div
            className="absolute top-0 bottom-0 w-px bg-marine-400 pointer-events-none"
            style={{ left: `${getPosition(times[currentIndex])}%` }}
          />
        </div>

        {/* Controls */}
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => !disabled && onFrameChange(0)}
            disabled={disabled || currentIndex === 0}
            className="btn-secondary p-2 disabled:opacity-30"
            title="First frame"
          >
            <SkipBack className="w-4 h-4" />
          </button>
          <button
            onClick={() => !disabled && onFrameChange(Math.max(0, currentIndex - 1))}
            disabled={disabled || currentIndex === 0}
            className="btn-secondary p-2 disabled:opacity-30"
            title="Previous frame"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={() => {}} // Play/pause would animate frames
            disabled={disabled}
            className="btn-primary p-2 disabled:opacity-30"
            title={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>
          <button
            onClick={() => !disabled && onFrameChange(Math.min(frames.length - 1, currentIndex + 1))}
            disabled={disabled || currentIndex === frames.length - 1}
            className="btn-secondary p-2 disabled:opacity-30"
            title="Next frame"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
          <button
            onClick={() => !disabled && onFrameChange(frames.length - 1)}
            disabled={disabled || currentIndex === frames.length - 1}
            className="btn-secondary p-2 disabled:opacity-30"
            title="Last frame"
          >
            <SkipForward className="w-4 h-4" />
          </button>
          <button
            onClick={() => !disabled && onFrameChange(frames.length - 1)}
            disabled={disabled}
            className="btn-secondary p-2 disabled:opacity-30"
            title="Fast forward"
          >
            <FastForward className="w-4 h-4" />
          </button>
        </div>

        {/* Current time display */}
        <div className="text-center">
          <span className="text-lg font-mono font-semibold text-marine-400">
            {times[currentIndex]}h / {maxTime}h
          </span>
          <p className="text-xs text-dark-text-muted">Simulation Time</p>
        </div>
      </div>
    </div>
  );
}